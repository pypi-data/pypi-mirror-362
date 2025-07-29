import json
import os
import sys
import webbrowser

import rich_click as click

import cli.ui as ui
from api.project_api import ProjectApi
from .config import Config
from .check import (
    WakeExport,
    WakeExportError,
    wait_for_server_execution,
    wait_for_server_upload_confirm,
    download_and_unzip_zip_result,
    upload_export,
)

@click.command("submit")
@click.argument("file", type=click.Path(exists=True))
@click.option("-n", "--name", help="Name for the performed check", type=str)
@click.option("-p", "--project", help="Project", type=str)
@click.option(
    "-f",
    "--format",
    help="format of result, json with png result will be downloaded to your local machine",
    default="web",
    type=click.Choice(["web", "json_with_png"], case_sensitive=False),
)
@click.pass_context
def submit(ctx, file, name, project, format):
    """Submit previously generated sources.json for detections scanning in Wake Arena"""

    try:
        config: Config = ctx.obj.get("config")
        project_api: ProjectApi = ctx.obj.get("project_api")

        with open(file, "r") as f:
            data = json.load(f)
            wake_version = data["version"]

        project_id: str = project if project else config.get_active_project()
        print(f"project_id: {project_id}")

        export = WakeExport(file).validate()

        check_id = upload_export(project_api, project_id, export, name, format, wake_version)

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
