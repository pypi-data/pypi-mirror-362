"""Information commands for {{ project_name }}."""

import platform
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from {{ package_name }}.config import get_config

app = typer.Typer(help="Show information about the system and application")
console = Console()


@app.command()
def system() -> None:
    """Show system information."""
    console.print("💻 [bold blue]System Information[/bold blue]\n")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("Platform:", platform.platform())
    table.add_row("Architecture:", platform.machine())
    table.add_row("Python Version:", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    table.add_row("Python Executable:", sys.executable)

    console.print(table)


@app.command()
def config() -> None:
    """Show configuration information."""
    config_data = get_config()

    console.print("⚙️  [bold blue]Configuration[/bold blue]\n")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("Config File:", str(config_data.config_file))
    table.add_row("Debug Mode:", "✅ Enabled" if config_data.debug else "❌ Disabled")
    table.add_row("Output Format:", config_data.output_format)

    console.print(table)


@app.command()
def version() -> None:
    """Show version information."""
    from {{ package_name }} import __version__

    console.print(f"{{ project_name }} version [green]{__version__}[/green]")


@app.command()
def paths() -> None:
    """Show application paths."""
    from {{ package_name }}.config import get_cache_dir, get_data_dir

    console.print("📁 [bold blue]Application Paths[/bold blue]\n")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("Data Directory:", str(get_data_dir()))
    table.add_row("Cache Directory:", str(get_cache_dir()))
    table.add_row("Current Directory:", str(Path.cwd()))

    console.print(table)
