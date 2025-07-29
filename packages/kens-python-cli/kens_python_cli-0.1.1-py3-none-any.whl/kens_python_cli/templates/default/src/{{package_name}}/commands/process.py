"""File processing commands for {{ project_name }}."""

{% if use_async %}import asyncio
{% endif %}from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

app = typer.Typer(help="Process files and data")
console = Console()


@app.command()
def files(
    paths: List[Path] = typer.Argument(
        ...,
        help="Paths to process",
        exists=True,
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Process directories recursively",
    ),
    pattern: Optional[str] = typer.Option(
        None,
        "--pattern",
        "-p",
        help="File pattern to match (e.g., '*.txt')",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be processed without doing it",
    ),
) -> None:
    """Process files from given paths."""
    all_files = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)

        for path in paths:
            if path.is_file():
                all_files.append(path)
            elif path.is_dir() and recursive:
                if pattern:
                    all_files.extend(path.rglob(pattern))
                else:
                    all_files.extend(path.rglob("*"))
            elif path.is_dir():
                if pattern:
                    all_files.extend(path.glob(pattern))
                else:
                    all_files.extend(path.glob("*"))

    # Filter out directories
    all_files = [f for f in all_files if f.is_file()]

    if not all_files:
        console.print("❌ No files found to process")
        return

    # Display results
    table = Table(title=f"Found {len(all_files)} files")
    table.add_column("File", style="cyan")
    table.add_column("Size", justify="right")
    table.add_column("Modified", justify="right")

    for file_path in all_files[:10]:  # Show first 10 files
        try:
            stat = file_path.stat()
            size = f"{stat.st_size:,} bytes"
            modified = f"{stat.st_mtime:.0f}"
            table.add_row(str(file_path), size, modified)
        except OSError:
            table.add_row(str(file_path), "N/A", "N/A")

    if len(all_files) > 10:
        table.add_row("...", f"+{len(all_files) - 10} more", "")

    console.print(table)

    if dry_run:
        console.print("🔍 [yellow]Dry run - no files were actually processed[/yellow]")
    else:
        console.print(f"✅ Would process {len(all_files)} files")


@app.command()
def count(
    directory: Path = typer.Argument(
        Path.cwd(),
        help="Directory to count files in",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Count files recursively",
    ),
) -> None:
    """Count files in a directory."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Counting files...", total=None)

        if recursive:
            files = list(directory.rglob("*"))
        else:
            files = list(directory.glob("*"))

    # Separate files and directories
    file_count = sum(1 for f in files if f.is_file())
    dir_count = sum(1 for f in files if f.is_dir())

    console.print(f"📊 [bold blue]File Count Results[/bold blue]\n")
    console.print(f"Directory: [cyan]{directory}[/cyan]")
    console.print(f"Files: [green]{file_count:,}[/green]")
    console.print(f"Directories: [yellow]{dir_count:,}[/yellow]")
    console.print(f"Total items: [blue]{len(files):,}[/blue]")

    if recursive:
        console.print("🔄 [dim](recursive scan)[/dim]")


{% if use_async %}@app.command()
def async_example(
    delay: float = typer.Option(
        1.0,
        "--delay",
        "-d",
        help="Delay in seconds for async operation",
    ),
) -> None:
    """Example of async operation."""
    async def async_operation() -> None:
        console.print("⏳ Starting async operation...")
        await asyncio.sleep(delay)
        console.print("✅ Async operation completed!")

    asyncio.run(async_operation())
{% endif %}
