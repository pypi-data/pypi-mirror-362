import logging

from cli import ui
from wake_versions.manager import WakeVersionManager

logging.basicConfig(
    format="%(asctime)s,%(msecs)d [%(levelname)s] %(name)s: %(message)s",
    level=logging.CRITICAL,
)

import rich_click as click

from api.project_api import ProjectApi, ProjectApiError
from cli.check import check as check_command
from cli.config import config as config_command
from cli.init import init as init_command
from cli.project import project as project_command
from cli.submit import submit as submit_command
from cli.wake import wake as wake_command
from config.config import Config


@click.group()
@click.version_option(message="%(version)s", package_name="wake-arena-cli")
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

    logger = logging.getLogger("CLI")
    config = Config()
    client = config.get_active_client()
    version_manager = WakeVersionManager(config)

    ctx.obj["logger"] = logger
    ctx.obj["config"] = config
    ctx.obj["version_manager"] = version_manager
    ctx.obj["project_api"] = (
        ProjectApi(
            logger=logger,
            server_url=config.get_api_url(),
            token=client["token"],
            oauth_client_secret=config.get_oauth_secret(),
        )
        if client
        else None
    )


main.add_command(init_command)
main.add_command(check_command)
main.add_command(config_command)
main.add_command(project_command)
main.add_command(submit_command)
main.add_command(wake_command)

if __name__ == "__main__":
    main()
