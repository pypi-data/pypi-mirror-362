import re
import uuid
import os
import datetime

import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import NestedCompleter, FuzzyWordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.markup import MarkdownLexer
from rich.console import Console
from rich.markdown import Markdown

from .copilot import Copilot
from .config import RUNTIME_DIR, CONFIG_DIR


def get_filepaths(directory):
    file_paths = []
    gitignore_patterns = [re.compile(r"\.git/")]
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Convert gitignore pattern to regex pattern
                        pattern = line.replace(".", r"\.").replace("*", ".*")
                        gitignore_patterns.append(re.compile(pattern))
        except Exception as _:
            pass

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Check if file matches any gitignore pattern
            relative_path = os.path.relpath(filepath, directory)
            if not any(pattern.search(relative_path) for pattern in gitignore_patterns):
                file_paths.append(filepath)

    return file_paths


class Chat:
    def __init__(
        self,
        copilot: Copilot,
        model: str = "gpt-4-o-preview",
        session_id: str | None = None,
    ):
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = uuid.uuid4().hex[0:6]
        self.history_location = RUNTIME_DIR / f".pycopilot-{self.session_id}.history"
        self.save_to_history("System", copilot.system_prompt)

        self.session: PromptSession = PromptSession(
            history=FileHistory(CONFIG_DIR / ".pycopilot.history"),
            auto_suggest=AutoSuggestFromHistory(),
            lexer=PygmentsLexer(MarkdownLexer),
            reserve_space_for_menu=4,
        )
        self.console = Console()
        self.copilot = copilot
        self.model = model

        self._completer = NestedCompleter.from_nested_dict(
            {
                "/file": FuzzyWordCompleter(get_filepaths(".")),
                "/model": FuzzyWordCompleter(
                    [model["id"] for model in self.copilot.models]
                ),
                "/reset": None,
            },
        )

    def bottom_toolbar(self):
        working_width = os.get_terminal_size().columns

        model_display = f"Model: {self.model}"
        spacer = " " * (
            working_width - len(model_display) - 22
        )  # 41 is the length of the controls text
        return HTML(
            f"<b><kbd>^ C</kbd></b> Exit | <b><kbd>⌥ ⏎</kbd></b> Submit{spacer}{model_display}"
        )

    def handle_console_input(self) -> str:
        style = Style.from_dict({"prompt": "green bold"})
        with prompt_toolkit.patch_stdout.patch_stdout():
            return self.session.prompt(
                HTML(f"<prompt>{self.copilot.auth.user.login}></prompt> "),
                multiline=False,
                bottom_toolbar=self.bottom_toolbar,
                style=style,
                completer=self._completer,
                complete_while_typing=True,
                complete_in_thread=True,
            ).strip()

    def handle_streaming(self, prompt):
        stream = self.copilot.generate_ask(prompt, model=self.model)

        self.console.print()
        self.console.print("Copilot> ", style="bold blue")
        self.console.print()
        text = ""
        for response in stream:
            text = text + response
            self.console.print(response, end="")
        self.console.print()
        return text

    def save_to_history(self, kind, text):
        with open(self.history_location, "a") as f:
            # write current time
            timestamp = datetime.datetime.now().ctime()
            f.write(f"# {timestamp}\n")
            # write kind and text
            f.write(f"{kind}: {text}\n\n")

    def command(self, text):
        if text.startswith("/reset"):
            self.copilot.reset()
            self.console.print("[green]Resetting Copilot History[/green]")
            self.save_to_history("Meta", "Resetting Copilot History")

        if text.startswith("/model"):
            self.model = text.split(" ")[1]
            return

        if text.startswith("/file"):
            file_path = text[6:].strip()
            try:
                with open(os.path.expanduser(file_path), "r") as file:
                    text = file.read()
                    content = (
                        f"The contents of the file {file_path} are:\n\n```{text}\n```"
                    )
                    self.copilot.feed(content)
                    self.console.print(
                        f"[green]Reading file into context:[/green] {file_path}"
                    )
                    return text
            except (FileNotFoundError, PermissionError) as e:
                self.console.print(f"[red]Error reading file:[/red] {e}")

    def chat(self):
        self.console.print(Markdown("## Welcome to GitHub Copilot Chat!"))

        while True:
            try:
                prompt = self.handle_console_input()

                if prompt.startswith("/"):
                    prompt = self.command(prompt)
                    continue

                if not prompt:
                    continue

                self.save_to_history("User", prompt)
                response = self.handle_streaming(prompt=prompt)
                self.save_to_history("Assistant", response)

            # NOTE: Ctrl + c (keyboard) or Ctrl + d (eof) to exit
            # Adding EOFError prevents an exception and gracefully exits.
            except (KeyboardInterrupt, EOFError):
                self.console.print(
                    f"[green]✓[/green] Chat history saved to: {self.history_location}"
                )
                exit()


if __name__ == "__main__":
    chat = Chat()
    chat.chat()
