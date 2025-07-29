import rich_click as click

import api
from cli import ui
from config.config import Config


@click.group("project")
def project():
    """Commands to operate your projects"""

    pass


@project.command("select")
@click.pass_context
def project_select(ctx):
    """Opens dialog for project selection"""

    config: Config = ctx.obj.get("config")
    project_api: api.ProjectApi = ctx.obj.get("project_api")

    active_client = config.get_active_client()

    if not active_client or not project_api:
        ui.error("No active API key, run INIT command first")
        return

    with ui.spinner("Loading your projects"):
        projects = project_api.list_projects()

    if len(projects) == 0:
        ui.box(
            title="No project found",
            desc="Please create a new project with PROJECT CREATE command",
        )

    selected_project = ui.ask_select(
        title="Select Wake Arena project",
        choices=[
            (f"({project['id']}) {project['name']}", project) for project in projects
        ],
    )

    if selected_project == None:
        return

    config.set_active_project(selected_project["id"])
    config.write()

    ui.success(
        "Project was set 🛠️",
        [
            "Current Wake Arena project is "
            + ui.highlight(selected_project["name"] + f" ({selected_project['id']})")
        ],
    )


@project.command("create")
@click.option("-n", "--name", type=str, help="Name of the project")
@click.pass_context
def project_create(ctx, name):
    """Creates new project"""

    config: Config = ctx.obj.get("config")
    project_api: api.ProjectApi = ctx.obj.get("project_api")

    active_client = config.get_active_client()

    if not active_client or not project_api:
        ui.error(f"No active API key, run {ui.command('init')} command first")
        return

    if not name:
        name = ui.ask_with_help(
            title="Wake Arena Project Name",
            desc="Virtual space where we store all of your Wake runs and audits",
            enter="Enter the project name",
        )

    project = project_api.create_project(name)
    config.set_active_project(project.get("id"))
    config.write()
    ui.success(
        title="Successfully created! 🎉",
        lines=["Current project set to " + ui.highlight(project.get("name"))],
    )
