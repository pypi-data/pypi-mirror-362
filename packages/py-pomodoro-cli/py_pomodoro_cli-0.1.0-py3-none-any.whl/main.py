import time
from datetime import datetime

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.style import Style

# Nord Frost color scheme
NORD_FROST_START = "#5E81AC"
NORD_FROST_END = "#8FBCBB"

console = Console()


def run_pomodoro(interval: int):
    """Runs the Pomodoro timer for the specified interval."""
    console.print(
        "🚀 Starting Pomodoro timer...", style=f"bold {NORD_FROST_START}"
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(
            style=Style(color=NORD_FROST_START),
            complete_style=Style(color=NORD_FROST_END),
        ),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "[green]Pomodoro in progress...", total=interval * 60
        )
        for _ in range(interval * 60):
            time.sleep(1)
            progress.update(task, advance=1)

    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(
        f"🎉 The current Pomodoro interval has completed - {completion_time}",
        style=f"bold {NORD_FROST_END}",
    )


def pomodoro(
    interval: int = typer.Option(
        25,
        "--interval",
        "-i",
        help="The Pomodoro interval in minutes.",
    )
):
    """A simple Pomodoro CLI tool."""
    run_pomodoro(interval)


def main():
    """Main entry point for the application."""
    typer.run(pomodoro)


if __name__ == "__main__":
    main()
