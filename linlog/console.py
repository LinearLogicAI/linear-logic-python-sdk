import sys
from rich.console import Console
from rich.theme import Theme


base_theme = Theme({
    "info": "dim blue",
    "warning": "magenta",
    "error": "bold red"
})

console = Console(theme=base_theme)


def log_error(message: str) -> None:
    console.print(f"ERROR: {message}", style="error")
    sys.exit(1)
