import typer
from rich.console import Console
from rich.text import Text
from rich.align import Align

console = Console()

def info():
    """Display a large TAVIX logo and project information."""

    logo = r"""
[green]████████╗   █████╗   ██╗   ██╗ ██╗ ██╗  ██╗[/green]
[green]╚══██╔══╝  ██╔══██╗  ██║   ██║ ██║ ╚██╗██╔╝[/green]
[green]   ██║     ███████║  ██║   ██║ ██║  ╚███╔╝ [/green]
[green]   ██║     ██╔══██║  ╚██╗ ██╔╝ ██║  ██╔██╗ [/green]
[green]   ██║     ██║  ██║   ╚████╔╝  ██║ ██╔╝ ██╗[/green]
[green]   ╚═╝     ╚═╝  ╚═╝    ╚═══╝   ╚═╝ ╚═╝  ╚═╝[/green]
    """

    logo_text = Text.from_markup(logo, justify="center")
    console.print(logo_text)

    info_text = Text.from_markup(
        """An AI-powered shell assistant and coding companion using Google Gemini.

Read the documentation on [bold link=https://github.com/Atharvadethe/Tavix]GitHub[/bold link] or [bold link=https://pypi.org/project/tavix/]PyPI[/bold link] for more info.

Made by [bold]Atharva Dethe[/bold]""",
        justify="center"
    )

    console.print("\n") # Add a little space
    console.print(Align.center(info_text))