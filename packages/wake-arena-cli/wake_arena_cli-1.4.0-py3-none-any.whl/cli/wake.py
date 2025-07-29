import readline
import sys

import packaging
import rich_click as click

import api
import cli.ui as ui
from config import Config
from wake_versions.exceptions import UnsupportedWakeVersion, VersionNotInstalledError
from wake_versions.manager import WakeVersionManager, get_wake_machine_info

_MSG_NOT_SUPPORTED = "(Not supported)"
_MSG_INSTALLED = "[Installed]"


def _log_wake_version(
    version_name: str, only_supported: bool, is_installed: bool = False
):
    installed_postfix = " " + ui.highlight(_MSG_INSTALLED) if is_installed else ""

    if packaging.version.parse(version_name) < Config.WAKE_MIN_VERSION:
        if not only_supported:
            ui.line(
                version_name + " " + ui.warning(_MSG_NOT_SUPPORTED) + installed_postfix
            )
    else:
        ui.line(version_name + installed_postfix)


@click.group("wake")
@click.pass_context
def wake(ctx):
    """
    Wake version installation and activation
    """
    pass


@wake.command("install")
@click.argument("version", required=False, default="")
@click.pass_context
def install(ctx, version):
    """Installs specific Wake version to your local system"""

    manager = ctx.obj.get("version_manager")

    with ui.spinner("Loading available Wake versions"):
        remote_versions = manager.list_remote(version)
        local_versions = manager.list_local()
        versions = [v for v in remote_versions if v not in local_versions]
        available_choices = [
            (
                (v, v)
                if packaging.version.parse(v) >= Config.WAKE_MIN_VERSION
                else (v + " " + _MSG_NOT_SUPPORTED, v)
            )
            for v in versions
        ]
    if len(available_choices) == 0:
        ui.error("No Wake versions available to install")
        return
    if not version or len(versions) > 1:
        version = ui.ask_select(
            "Which version to install",
            choices=available_choices,
        )
        if version == None:
            return
    elif len(available_choices) == 1:
        version = available_choices[0][0]
    elif version not in available_choices:
        if version in local_versions:
            ui.error(f"Wake version {version} is already installed")
            return

        ui.error(f"Wake version {version} is not available for your platform")
        return

    with ui.spinner(f"Installing version {version}"):
        manager.install(version)

    ui.success(
        title="Wake version installed",
        lines=[f"Wake version {version} successfuly installed"],
    )


@wake.command("uninstall")
@click.argument("version", required=False, default=None)
@click.pass_context
def uninstall(ctx, version):
    """Uninstalls specific Wake version from your local system"""
    manager = ctx.obj.get("version_manager")

    if version is None:
        local_versions = manager.list_local()
        version = ui.ask_select("Which version to uninstall", choices=local_versions)

    with ui.spinner(f"Uninstalling {version}"):
        result = manager.uninstall(version)

    if result:
        ui.success(
            f"{result} uninstalled",
            lines=[f"Wake version {result} was successfuly uninstalled"],
        )
    else:
        ui.error(
            f"{version} not found",
            lines=[f"Wake version {version} is not installed on this device"],
        )


@wake.command("use")
@click.argument("version", required=False, default=None)
@click.pass_context
def use(ctx, version):
    """Activates specific Wake version, use 'default' if you want to use Wake version available in current terminal"""
    manager: WakeVersionManager = ctx.obj.get("version_manager")

    if version == "default":
        manager.deactivate()
        ui.line("Using current terminal version")
        wake_version = manager.get_shell_version()

        if wake_version:
            ui.line(wake_version)
        else:
            ui.line(ui.warning("No Wake version installed in current terminal"))
        return

    if version is not None:
        manager.activate(version)
    else:
        local_versions = manager.list_local()

        if len(local_versions) == 0:
            ui.error(
                "No version installed", lines=["Please use WAKE INSTALL command first"]
            )
            sys.exit(1)

        version = ui.ask_select("Which version to activate", choices=local_versions)
        if not version:
            return

    with ui.spinner(f"Activating version {version}"):
        manager.activate(version)

    ui.success(
        f"Version {version} activated",
        lines=[f"Wake Arena is now using Wake version {version}"],
    )


@wake.command("shell")
@click.argument(
    "version",
    required=False,
    default=None,
)
@click.pass_context
def shell(ctx, version):
    """Activates shell with installed wake version, if [VERSION] is not provided, current active Wake Arena Wake version is used"""
    manager: WakeVersionManager = ctx.obj.get("version_manager")
    manager.shell(version)


@wake.command("version")
@click.pass_context
def version(ctx):
    """Shows currently activated wake version"""
    config: Config = ctx.obj.get("config")
    manager: WakeVersionManager = ctx.obj.get("version_manager")

    wake_version = config.get_wake_version()
    if not wake_version:
        wake_version = manager.get_shell_version()

    if not wake_version:
        raise VersionNotInstalledError()

    current = packaging.version.parse(wake_version)

    if not current:
        ui.error(
            title=f"Invalid version of Wake ${wake_version}",
            desc="Please WAKE USE command to activate valid version of Wake",
        )
        return

    ui.line(current)


@wake.command("list")
@click.option(
    "-a",
    "--available",
    is_flag=True,
    default=False,
    show_default=True,
    help="Lists all available Wake versions for your platform including uninstalled versions",
)
@click.option(
    "-s",
    "--only-supported",
    is_flag=True,
    default=False,
    show_default=True,
    help="Lists only versions supported by Wake Arena",
)
@click.pass_context
def list(ctx, available: bool, only_supported: bool):
    """Lists available Wake versions"""

    config: Config = ctx.obj.get("config")
    project_api: api.ProjectApi = ctx.obj.get("project_api")

    active_client = config.get_active_client()
    active_project = config.get_active_project()
    manager = ctx.obj.get("version_manager")

    if not active_client or not active_project or not project_api:
        ui.error("Configuration not complete, please use INIT command first")
        return

    if available:
        with ui.spinner("Loading available Wake versions"):
            remote_versions = manager.list_remote()
            local_versions = manager.list_local()
            terminal_version = manager.get_shell_version()

        machine_info = get_wake_machine_info()
        ui.section_start(
            text=f"Available Wake versions for Python {machine_info['platform']} {machine_info['arch']}"
        )
        for version_name in remote_versions:
            _log_wake_version(
                version_name,
                only_supported,
                is_installed=version_name in local_versions,
            )

        ui.section_end()
        return

    with ui.spinner("Loading local Wake versions"):
        local_versions = manager.list_local()

    if len(local_versions) == 0:
        ui.error(
            "No local version found, run WAKE INSTALL [version] command to install wake first"
        )
        return
    ui.section_start(text="Installed Wake versions")
    for version_name in local_versions:
        _log_wake_version(version_name, only_supported)

    ui.section_end()
