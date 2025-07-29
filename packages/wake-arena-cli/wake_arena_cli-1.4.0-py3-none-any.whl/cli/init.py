import getpass
import platform
import sys
import time
from logging import Logger

import rich_click as click

import api

sys.path.append("../cli")

import webbrowser

from dateutil.parser import parse

import cli.ui as ui
from api.project_api import ProjectApi, ProjectApiError
from config import Config

DEMO_CLIENT_NAME = "demo"
DEMO_CLIENT_USER = "demo@ackee.xyz"


class AuthError(click.ClickException):
    def __init__(self, message: str, help: str):
        super().__init__(message)
        self.help = help


@click.command("init")
@click.pass_context
def init(ctx):
    """Initializes CLI authentication"""

    logger: Logger = ctx.obj.get("logger")
    config: Config = ctx.obj.get("config")

    name = ui.ask_with_help(
        title="Wake Arena Device name",
        desc="This name can help you recognize the devices you are working with. You will see the name on every code check made by this CLI in the Wake Arena App",
        enter="Enter the name of your device",
        default=f"{getpass.getuser()}@{platform.node()}",
    )

    project_api = ProjectApi(logger, config.get_api_url())

    oauth = {}
    with ui.spinner("Getting the OAuth device code"):
        oauth = project_api.get_device_code(name=name)

    verification_code = oauth["userCode"]
    styled_code = " ".join(
        [verification_code[i : i + 3] for i in range(0, len(verification_code), 3)]
    )

    verification_url = f"{oauth['authenticationUri']}?userCode={verification_code}"
    webbrowser.open(verification_url, new=0, autoraise=True)
    ui.box(
        "Please verify the device code with your account in browser",
        desc="Your verification code is",
        main_text=styled_code,
        bottom_text=f"If the browser didn't open automatically, visit: {verification_url}",
    )

    token = wait_for_code_approval(project_api, oauth)

    projects = []
    project_api = api.ProjectApi(
        logger=logger, server_url=config.get_api_url(), token=token
    )

    user_profile = project_api.get_user_profile()
    config.add_client(
        name=name,
        user=user_profile["email"],
        token=token,
    )

    with ui.spinner("Listing user projects"):
        try:
            projects = project_api.list_projects()
        except api.project_api.ProjectApiError:
            ui.error("Error occured when listing the projects")
            return
    project = {}
    if len(projects) > 0:
        project = projects[0]
    else:
        project_name = ui.ask_with_help(
            title="Wake Arena Project Name",
            desc="Virtual space where we store all of your Wake runs and audits",
            enter="Enter the project name",
        )
        try:
            project = project_api.create_project(project_name)
        except ProjectApiError:
            ui.error("Error occured when creating the project")
            return
    config.set_active_client(name)
    config.set_active_project(project.get("id"))
    config.write()
    ui.success(
        title="Successfully initialized! 🎉",
        lines=[
            "Current project set to "
            + ui.highlight(project.get("name"))
            + f' ({project.get("id")})',
            "You can switch the project using "
            + ui.command("config project switch")
            + " command",
            "To perform Wake test go to folder with your code, install dependencies and use "
            + ui.command("check")
            + " command",
            "To configure your build use wake.toml. Check documentation at https://ackee.xyz/wake/docs/latest/configuration/"
        ],
    )


def wait_for_code_approval(project_api: ProjectApi, oauth: dict) -> str:
    with ui.spinner("Waiting for user approval of device") as spinner:
        expiration_time = parse(oauth["expiresIn"])
        spinner.update("Waiting for user approval of device")

        while True:
            if time.time() > expiration_time.timestamp():
                ui.error("Device code expired: User didn't approve the device in time")
                sys.exit()
            try:
                response = project_api.generate_api_token(oauth["deviceCode"])
            except ProjectApiError as err:
                if err.code == "AUTHORIZATION_PENDING":
                    time.sleep(oauth["pollIntervalInS"])
                    continue
                if err.code == "TOO_MANY_REQUESTS":
                    time.sleep(2 * oauth["pollIntervalInS"])
                    continue
                elif err.code == "AUTHORIZATION_DECLINED":
                    ui.error("Device code was declined by the user")
                    sys.exit()
                elif err.code == "AUTHORIZATION_EXPIRED":
                    ui.error(
                        "Device code expired: User didn't approve the device in time"
                    )
                    sys.exit()
                raise err
            return response["token"]
