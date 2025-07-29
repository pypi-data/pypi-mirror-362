import json
import os
import subprocess
import sys
import time
import webbrowser
import zipfile
from enum import Enum
from pathlib import Path

import dateutil.parser
import requests
import rich_click as click
from packaging import version
from typing_extensions import Self

import cli.ui as ui
from api.project_api import ProjectApi, ProjectApiError
from config import Config
from wake_versions.manager import WakeVersionManager

WAKE_EXPORT_DIR = ".wake"
WAKE_FILE = os.path.join(WAKE_EXPORT_DIR, "sources.json")
CHECK_TIMEOUT_IN_S = 60 * 10  # 10 minutes
UPLOAD_CONFIRM_TIMEOUT_IN_S = 60 * 3  # 3 minutes


class CheckState(Enum):
    VERIFICATION = "VERIFICATION"
    WAITING_FOR_UPLOAD = "WAITING_FOR_UPLOAD"
    WAITING_FOR_CHECK = "WAITING_FOR_CHECK"
    FETCHING_CODE = "FETCHING_CODE"
    CHECKING = "CHECKING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class WakeExportError(click.ClickException):
    def __init__(self, message: str, help: str | None):
        super().__init__(message)
        self.help = help


class WakeExport:
    def __init__(self, file: str):
        self.file = file
        self.sources = {}
        self.file_size = 0

        if not Path(self.file).is_file():
            return

        with open(self.file) as content:
            self.sources = json.load(content)
            self.file_size = Path(self.file).stat().st_size

    def validate(self) -> Self:
        if not self.sources:
            raise WakeExportError(
                "No compilation export file found, nothing to check",
                "Check the compilation output for errors",
            )

        if version.parse(self.sources.get("version")) < Config.WAKE_MIN_VERSION:
            raise WakeExportError(
                "Unsupported Wake version in export",
                f"Run export again with Wake version >= ${Config.WAKE_MIN_VERSION}",
            )

        sources = self.sources.get("sources")

        if not sources or len(sources) == 0:
            raise WakeExportError(
                "Empty export",
                "The directory is empty or contains only dependencies. If you still want to check just dependencies, change compiler.solc.exclude_paths a detectors.exclude_paths in your wake.toml configuration. Check Wake configuration at https://ackee.xyz/wake/docs/latest/configuration",
            )

        return self

    def upload(self, url: str):
        headers = {"Content-Type": "application/json"}
        res = requests.put(url, data=json.dumps(self.sources), headers=headers)

        if res.status_code != 200:
            raise WakeExportError("Upload not successful", res.content)


def is_final_state(state: str):
    return state in [CheckState.FINISHED.value, CheckState.ERROR.value]


def upload_export(
    project_api: ProjectApi,
    project_id: str,
    export: WakeExport,
    name: str | None,
    format: str,
    active_version: str,
):
    check_id = None

    with ui.spinner("Requesting upload") as spinner:
        upload = project_api.get_upload_link(project_id, name, format, active_version)

        upload_link = upload.get("link")
        check_id = upload.get("checkId")

        if not upload_link or not check_id:
            raise WakeExportError("Upload was not successful", "Please try again")

        spinner.update("Uploading")
        export.upload(upload_link)

    return check_id


def wait_for_server_upload_confirm(api: ProjectApi, project_id: str, check_id: str):
    state = None

    with ui.spinner("Waiting for server confirmation"):
        timeout = time.time() + UPLOAD_CONFIRM_TIMEOUT_IN_S

        while True:
            if time.time() > timeout:
                raise WakeExportError(
                    "Timeout: Server didn't confirmed export upload", "Please try again"
                )

            check = api.get_vulnerability_check(project_id, check_id)
            status = check.get("status")

            if status != "PREPARATION":
                break

            time.sleep(1)

    return state


def wait_for_server_execution(project_api: ProjectApi, project_id: str, check_id: str):
    with ui.spinner("Waiting for the remote execution") as spinner:
        timeout = time.time() + CHECK_TIMEOUT_IN_S

        last_log_time = None
        check_state = None

        while True:
            if time.time() > timeout:
                raise WakeExportError(
                    "Timeout: Server didn't executed the check",
                    "Please try again or contact ABCH",
                )
            state_logs = project_api.get_vulnerability_check_state_logs(
                project_id, check_id, last_log_time
            )

            new_logs = state_logs.get("logs")
            if len(new_logs):
                for log in new_logs:
                    log_time = dateutil.parser.parse(log.get("createTime"))
                    ui.log(log_time, log.get("message"))
                last_log_time = new_logs[-1].get("createTime")

            curr_state = state_logs.get("state")
            if curr_state != check_state:
                check_state = curr_state
                if check_state == CheckState.CHECKING.value:
                    spinner.update("Server is checking the code")

            if is_final_state(check_state):
                break

            time.sleep(1)

        spinner.update("Getting results")
        check = project_api.get_vulnerability_check(project_id, check_id)
        check_state = check.get("status")

        if check_state == CheckState.ERROR.value:
            error = check.get("error")
            raise WakeExportError(
                "Remote execution failed",
                help=error if error else None,
            )

        return check


def download_and_unzip_zip_result(url: str):
    download_path = os.path.join(
        os.getcwd(), WAKE_EXPORT_DIR, "wake_arena_detections.zip"
    )
    extract_to_path = os.path.join(os.getcwd(), WAKE_EXPORT_DIR, "detections")

    # ensure the parent directory exists
    Path(download_path).parent.mkdir(parents=True, exist_ok=True)

    with ui.spinner("Downloading result") as spinner:
        response = requests.get(url, stream=True)
        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        spinner.update("Extracting result")
        with zipfile.ZipFile(download_path, "r") as zip_ref:
            zip_ref.extractall(extract_to_path)

        spinner.update("Clearing result zip")
        os.remove(download_path)


def is_forge_available():
    try:
        return subprocess.run(["forge", "--version"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


@click.command("check")
@click.option("-n", "--name", help="Name for the performed check", type=str)
@click.option("-p", "--project", help="Project", type=str)
@click.option("-c", "--compilation-only", is_flag=True, help="Run compilation only")
@click.option(
    "-f",
    "--format",
    help="format of result, json with png result will be downloaded to your local machine",
    default="web",
    type=click.Choice(["web", "json_with_png"], case_sensitive=False),
)
@click.pass_context
def check(ctx, name, project, compilation_only, format):
    """Performs remote Wake detection connected to Wake Arena project"""

    try:
        config: Config = ctx.obj.get("config")
        project_api: ProjectApi = ctx.obj.get("project_api")
        version_manager: WakeVersionManager = ctx.obj.get("version_manager")

        project_id = project if project else config.get_active_project()
        
        if not compilation_only:
            if not project_api or not project_id:
                ui.error("Please use INIT command first")
                return

            with ui.spinner("Checking configuration") as spinner:
                try:
                    project_api.get_project(project_id)
                except ProjectApiError as error:
                    spinner.stop()
                    if error.code == "NOT_FOUND":
                        ui.error(
                            title="Project not found",
                            lines=[
                                f"Project {project_id} does not exist, please call PROJECT SELECT command first"
                            ],
                        )
                        sys.exit(1)
                    else:
                        raise error
        active_version = config.get_wake_version()
        is_conda_version = True

        if not active_version:
            active_version = version_manager.get_shell_version()
            is_conda_version = False

        if not active_version:
            raise WakeExportError(
                "No Wake version found",
                "Install Wake using WAKE INSTALL command or select version using WAKE USE command",
            )

        if version.parse(active_version) < Config.WAKE_MIN_VERSION:
            raise WakeExportError(
                "Unsupported Wake version",
                f"Please install Wake version >= {active_version}",
            )
        ui.section_start(f"Compiling the source (Wake {active_version})")

        wake_command = "wake compile --export json"
        if is_conda_version:
            activation_command, _ = version_manager.get_activation_command(
                active_version
            )
            wake_command = f"{activation_command} && {wake_command}"
        else:
            activation_command = None

        if (
            version.parse(active_version) >= version.parse("4.16.1") and
            Path("foundry.toml").exists() and
            not Path("wake.toml").exists() and
            is_forge_available()
        ):
            subprocess.run(
                f"{activation_command} && wake up config" if activation_command else "wake up config",
                shell=True,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )

        if subprocess.run(
            wake_command,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        ).returncode != 0:
            raise WakeExportError(
                "Compilation failed",
                "Please check the compilation output for errors",
            )

        ui.section_end()

        output_file = os.path.join(os.getcwd(), WAKE_FILE)
        export = WakeExport(output_file).validate()
        if compilation_only:
            ui.success(title="Check completed", lines=["Upload skipped due to --compilation-only flag"])
            return
        # this creates the vulnerability check and uploads code
        check_id = upload_export(project_api, project_id, export, name, format, active_version)

        ui.section_start("Export uploaded, waiting for code check")

        wait_for_server_upload_confirm(project_api, project_id, check_id)
        check = wait_for_server_execution(project_api, project_id, check_id)

        ui.section_end()

        if format == "web":
            result_url = f"{config.get_web_url()}/project/{project_id}/check/{check_id}"
            ui.success(
                title="Check is completed",
                lines=["Results are available at", ui.highlight(result_url)],
            )
            webbrowser.open(result_url)
            return

        if format == "json_with_png":
            download_and_unzip_zip_result(check.get("resultLink"))
            ui.success(
                title="Check is completed",
                lines=[
                    "Results are available in .wake/detections folder",
                ],
            )

    except WakeExportError as err:
        ui.error(title=err.message, lines=[err.help] if err.help else [])
        sys.exit(1)
