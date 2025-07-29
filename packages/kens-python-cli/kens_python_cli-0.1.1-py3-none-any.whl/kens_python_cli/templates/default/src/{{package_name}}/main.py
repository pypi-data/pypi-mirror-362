"""Main CLI entry point for {{ project_name }}."""

{% if use_async %}import asyncio
{% endif %}from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.traceback import install

from {{ package_name }}.commands import info, process
from {{ package_name }}.config import get_config
from {{ package_name }}.utils.logging import setup_logging

# Install rich traceback handler
install()

# Create Typer app
app = typer.Typer(
    name="{{ project_name }}",
    help="🚀 {{ project_description }}",
    add_completion=False,
    rich_markup_mode="rich",
)

# Add subcommands
app.add_typer(info.app, name="info")
app.add_typer(process.app, name="process")

console = Console()


@app.command()
def hello(
    name: str = typer.Option(
        "World",
        "--name",
        "-n",
        help="Name to greet",
    ),
    count: int = typer.Option(
        1,
        "--count",
        "-c",
        help="Number of greetings",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """Say hello to someone."""
    if verbose:
        setup_logging(verbose=True)
        console.print(f"[dim]Greeting {name} {count} time(s)[/dim]")

    for i in range(count):
        greeting = f"Hello, {name}!"
        if count > 1:
            greeting = f"{i + 1}. {greeting}"
        console.print(f"👋 [green]{greeting}[/green]")


@app.command()
def config(
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Show current configuration",
    ),
) -> None:
    """Manage configuration."""
    if show:
        config_data = get_config()
        console.print("📋 [bold blue]Current Configuration[/bold blue]")
        console.print(f"Config file: [cyan]{config_data.config_file}[/cyan]")
        console.print(f"Debug mode: {config_data.debug}")
        console.print(f"Output format: {config_data.output_format}")
    else:
        console.print("Use --show to display current configuration")


@app.command()
def version() -> None:
    """Show version information."""
    from {{ package_name }} import __version__
    console.print(f"{{ project_name }} version [green]{__version__}[/green]")


{% if use_async %}async def async_main() -> None:
    """Async main entry point."""
    app()


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        console.print("\n❌ Operation cancelled by user")
        raise typer.Exit(1)
{% else %}def main() -> None:
    """Main entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n❌ Operation cancelled by user")
        raise typer.Exit(1)
{% endif %}


if __name__ == "__main__":
    main()

