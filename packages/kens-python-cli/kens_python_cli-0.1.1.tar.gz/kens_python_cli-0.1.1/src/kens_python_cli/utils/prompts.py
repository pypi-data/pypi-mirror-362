"""Interactive prompts for CLI configuration."""

import re
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from kens_python_cli.models.config import ProjectConfig

console = Console()


def get_project_name() -> str:
    """Get project name from user with validation."""
    while True:
        name = Prompt.ask(
            "📦 [bold blue]Project name[/bold blue]",
            default="my-cli-tool",
        )

        # Validate name
        if not name:
            console.print("[red]Project name cannot be empty[/red]")
            continue

        # Check for valid characters
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
            console.print(
                "[red]Project name must start with a letter and contain only "
                "letters, numbers, hyphens, and underscores[/red]"
            )
            continue

        return name


def get_project_description(project_name: str) -> str:
    """Get project description from user."""
    return Prompt.ask(
        "📝 [bold blue]Project description[/bold blue]",
        default=f"A modern Python CLI tool created with kens-python-cli",
    )


def get_author_info() -> tuple[str, str]:
    """Get author name and email from user."""
    author = Prompt.ask(
        "👤 [bold blue]Author name[/bold blue]",
        default="",
    )

    email = ""
    if author:
        email = Prompt.ask(
            "📧 [bold blue]Author email[/bold blue]",
            default="",
        )

    return author, email


def get_python_version() -> str:
    """Get Python version from user."""
    versions = ["3.11", "3.12", "3.13"]

    console.print("\n🐍 [bold blue]Python version[/bold blue]")
    table = Table(show_header=False, box=None, padding=(0, 2))

    for i, version in enumerate(versions, 1):
        status = "✅ Recommended" if version == "3.11" else ""
        table.add_row(f"[dim]{i}.[/dim]", f"Python {version}", status)

    console.print(table)

    while True:
        choice = Prompt.ask(
            "Choose Python version",
            choices=["1", "2", "3"],
            default="1",
        )
        return versions[int(choice) - 1]


def get_features() -> dict[str, bool]:
    """Get feature selections from user."""
    console.print("\n🔧 [bold blue]Features[/bold blue]")
    console.print("[dim]All features are recommended for modern Python development[/dim]\n")

    features = {
        "include_tests": Confirm.ask(
            "Include testing setup (pytest + coverage)?",
            default=True,
        ),
        "include_docs": Confirm.ask(
            "Include documentation setup?",
            default=True,
        ),
        "include_pre_commit": Confirm.ask(
            "Include pre-commit hooks (code quality)?",
            default=True,
        ),
        "include_github_actions": Confirm.ask(
            "Include GitHub Actions workflow?",
            default=False,
        ),
        "use_async": Confirm.ask(
            "Use async/await patterns?",
            default=False,
        ),
    }

    return features


def get_output_directory(project_name: str) -> Path:
    """Get output directory for project."""
    default_path = Path.cwd() / project_name

    path_input = Prompt.ask(
        "📁 [bold blue]Output directory[/bold blue]",
        default=str(default_path),
    )

    return Path(path_input).expanduser().resolve()


def collect_project_config() -> ProjectConfig:
    """Collect all project configuration from user."""
    console.print("\n🚀 [bold green]Create a new Python CLI project[/bold green]\n")

    # Basic info
    name = get_project_name()
    description = get_project_description(name)
    author, email = get_author_info()
    python_version = get_python_version()

    # Features
    features = get_features()

    # Create config
    config = ProjectConfig(
        name=name,
        description=description,
        author=author,
        email=email,
        python_version=python_version,
        **features,
    )

    return config


def confirm_project_creation(config: ProjectConfig, output_path: Path) -> bool:
    """Show project summary and confirm creation."""
    console.print("\n📋 [bold blue]Project Summary[/bold blue]")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("Name:", f"[green]{config.name}[/green]")
    table.add_row("Description:", config.description)
    table.add_row("Author:", f"{config.author} <{config.email}>" if config.email else config.author)
    table.add_row("Python Version:", f"≥{config.python_version}")
    table.add_row("Output Path:", f"[cyan]{output_path}[/cyan]")

    console.print(table)

    # Features
    console.print("\n🔧 [bold blue]Features[/bold blue]")
    features_table = Table(show_header=False, box=None, padding=(0, 2))

    feature_labels = {
        "include_tests": "Testing (pytest + coverage)",
        "include_docs": "Documentation",
        "include_pre_commit": "Pre-commit hooks",
        "include_github_actions": "GitHub Actions",
        "use_async": "Async/await patterns",
    }

    for key, label in feature_labels.items():
        status = "✅" if getattr(config, key) else "❌"
        features_table.add_row(status, label)

    console.print(features_table)

    return Confirm.ask(
        "\n🔨 [bold blue]Create project with these settings?[/bold blue]",
        default=True,
    )


def show_next_steps(project_path: Path, project_name: str) -> None:
    """Show next steps after project creation."""
    console.print("\n🎉 [bold green]Project created successfully![/bold green]\n")

    console.print("📝 [bold blue]Next steps:[/bold blue]")
    steps = [
        f"cd {project_path}",
        "uv sync  # Install dependencies",
        "uv run pytest  # Run tests",
        f"uv run {project_name.replace('-', '_')}  # Run your CLI",
    ]

    for i, step in enumerate(steps, 1):
        console.print(f"  [dim]{i}.[/dim] [cyan]{step}[/cyan]")

    console.print(f"\n📚 Check out the PROJECT_GUIDE.md for development help!")
    console.print("🤖 This guide is optimized for Claude Code development!\n")

