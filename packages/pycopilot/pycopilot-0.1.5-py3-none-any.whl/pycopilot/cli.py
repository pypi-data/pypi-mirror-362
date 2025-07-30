import typer
import questionary
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated, Optional
import pathlib

from .auth import Authentication
from .chat import Chat
from .copilot import Copilot
from .version import __version__


APP_NAME = "com.kdheepak.pycopilot"


def version_callback(value: bool):
    if value:
        print(f"pycopilot version: {__version__}")
        raise typer.Exit()


app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)


@app.callback()
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    """CLI for GitHub Copilot."""
    ...


@app.command()
def auth():
    """Autheticate with GitHub Copilot."""
    Authentication().auth()


@app.command()
def chat(
    prompt_file: Annotated[
        str | None,
        typer.Option(
            "--prompt-file",
            exists=True,
            readable=True,
            help="Path to a markdown file with a system prompt.",
        ),
    ] = None,
    model: Annotated[
        str,
        typer.Option(
            "--model",
            "-m",
            help="Model name to use for the chat",
            show_default=False,
        ),
    ] = "gpt-4-o-preview",
):
    """Chat with GitHub Copilot using a system prompt from a markdown file."""
    system_prompt = ""
    if prompt_file:
        with open(prompt_file, "r") as file:
            system_prompt = file.read()

    copilot = Copilot(system_prompt=system_prompt)
    models = copilot.models

    choices = [model["id"] for model in models]

    if model not in choices:
        model = questionary.select("Select model", choices=choices).ask()

    Chat(copilot=copilot, model=model).chat()


@app.command()
def list_chats():
    """List all chat sessions."""
    from .config import RUNTIME_DIR

    console = Console()
    table = Table(title="Chat Sessions")

    table.add_column("Session ID", style="cyan", no_wrap=True)
    table.add_column("History Location", style="green")

    for chat_file in pathlib.Path(RUNTIME_DIR).glob(".pycopilot-*.history"):
        session_id = chat_file.stem.split("-")[-1]

        table.add_row(session_id, str(chat_file))

    console.print(table)


@app.command()
def models():
    """List models available for chat in a Rich table."""
    models = Copilot().models

    console = Console()
    table = Table(title="Available Models")

    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Vendor", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Family", style="white")
    table.add_column("Max Tokens", style="white")
    table.add_column("Streaming", style="white")

    for model in models:
        capabilities = model.get("capabilities", {})
        family = capabilities.get("family", "N/A")
        max_tokens = capabilities.get("limits", {}).get("max_output_tokens", "N/A")
        streaming = capabilities.get("supports", {}).get("streaming", False)

        table.add_row(
            model.get("id", "N/A"),
            model.get("name", "N/A"),
            model.get("vendor", "N/A"),
            model.get("version", "N/A"),
            family,
            str(max_tokens),
            str(streaming),
        )

    console.print(table)


if __name__ == "__main__":
    app()
