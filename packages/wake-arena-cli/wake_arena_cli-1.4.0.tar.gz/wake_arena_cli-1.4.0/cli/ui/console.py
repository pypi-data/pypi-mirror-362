import datetime
from typing import Any

import inquirer
import rich
from inquirer.themes import Default, term
from rich.columns import Columns
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = rich.console.Console(highlight=False)
error_console = rich.console.Console(stderr=True)


class WakeArenaTheme(Default):
    def __init__(self):
        super().__init__()
        self.List.selection_color = term.bold_cyan
        self.List.selection_cursor = "❯"


def ask_select(title: str, choices: list[tuple[str, Any]]):
    if len(choices) == 0:
        error("No options available")
        return
    answers = inquirer.prompt(
        [
            inquirer.List(
                "q",
                message=title,
                choices=choices,
            ),
        ],
        theme=WakeArenaTheme(),
    )
    return answers["q"] if answers and "q" in answers else None


def ask_with_help(title: str, desc: str, enter: str, default: str | None = None):
    box(title, desc)
    return Prompt.ask(Text(enter, style="cyan"), default=default)


def box(
    title: str, desc: str, main_text: str | None = None, bottom_text: str | None = None
):

    panels = [
        Padding(Text(title, style="bold cyan"), (0, 1)),
        Padding(Text(desc, style="italic"), (0, 2)),
    ]

    if main_text != None:
        panels.append(Padding(Text(main_text, style="bold blue"), (1, 2)))

    if bottom_text != None:
        panels.append(Padding(Text(bottom_text, style="italic"), (0, 2)))

    console.print(
        Panel(
            Group(*panels),
            expand=False,
            border_style="dim white",
        )
    )


def spinner(title):
    return console.status(title, spinner_style="green")


def title(msg: str):
    console.print(msg, style="bold cyan")


def section_start(text: str):
    console.print(Panel(Text(text, style="bold cyan"), border_style="cyan"))
    console.rule(style="dim cyan bold")


def section_end():
    console.rule(style="dim cyan bold")


def success(title: str, lines: list):
    console.print(
        Panel(
            Group(
                Text(title, style="bold green"),
                Rule(style="dim green"),
                Padding(Group(*lines), (0, 1)),
            ),
            expand=False,
            border_style="dim green",
        )
    )


def highlight(text: str):
    return f"[bold blue]{text}[/]"


def warning(text: str):
    return f"[bold yellow]{text}[/]"


def command(text: str):
    return f"[bold cyan]{text.upper()}[/]"


def config(token: str, client: str, project: str, project_id: str, wake: str):
    table = Table(show_header=False, box=rich.box.SIMPLE_HEAD)
    table.add_column("", style="cyan", justify="right")
    table.add_column("", justify="right")
    table.add_row("token:", token)
    table.add_row("client:", client)
    table.add_row("project id:", project_id)
    table.add_row("project name:", project)
    table.add_row("wake version:", wake)

    console.print(table)


def line(message: str):
    console.print(message)


def log(time: datetime.datetime, message: str):
    time_str = time.strftime("%H:%M:%S")
    console.print(Columns([Text(f"{time_str}", style="dim cyan"), message]))


def error(title: str = None, lines: list = []):
    texts = []
    if title:
        texts.append(Text(title, style="bold red"))
    texts.extend(map(lambda m: Text(m, style="red"), lines))

    error_console.print(
        Panel(
            Group(*texts),
            expand=False,
            title_align="left",
            title=Text("ERROR", style="dim red bold"),
            highlight=True,
            border_style="red",
        )
    )
