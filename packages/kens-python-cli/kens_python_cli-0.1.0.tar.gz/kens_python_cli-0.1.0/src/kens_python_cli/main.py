"""Main CLI entry point for kens-python-cli."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.traceback import install

from kens_python_cli.models.config import ProjectConfig
from kens_python_cli.utils.file_ops import create_project_structure
from kens_python_cli.utils.prompts import (
    collect_project_config,
    confirm_project_creation,
    get_output_directory,
    show_next_steps,
)

# Install rich traceback handler
install()

# Create Typer app
app = typer.Typer(
    name="kens-python-cli",
    help="🐍 Modern Python CLI scaffolding tool for rapid development",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()


@app.command()
def create(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Name of the project to create",
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for the project",
    ),
    template: str = typer.Option(
        "default",
        "--template",
        "-t",
        help="Template to use",
    ),
    author: Optional[str] = typer.Option(
        None,
        "--author",
        "-a",
        help="Author name",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help="Author email",
    ),
    python_version: str = typer.Option(
        "3.11",
        "--python",
        "-p",
        help="Python version",
    ),
    no_tests: bool = typer.Option(
        False,
        "--no-tests",
        help="Skip testing setup",
    ),
    no_docs: bool = typer.Option(
        False,
        "--no-docs",
        help="Skip documentation setup",
    ),
    no_pre_commit: bool = typer.Option(
        False,
        "--no-pre-commit",
        help="Skip pre-commit hooks",
    ),
    github_actions: bool = typer.Option(
        False,
        "--github-actions",
        help="Include GitHub Actions workflow",
    ),
    async_support: bool = typer.Option(
        False,
        "--async",
        help="Use async/await patterns",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip interactive prompts and use defaults",
    ),
) -> None:
    """Create a new Python CLI project."""
    try:
        if yes and not project_name:
            console.print("[red]Error: --yes requires a project name[/red]")
            raise typer.Exit(1)

        if yes:
            # Non-interactive mode
            config = ProjectConfig(
                name=project_name,
                description=f"A modern Python CLI tool created with kens-python-cli",
                author=author or "",
                email=email or "",
                python_version=python_version,
                include_tests=not no_tests,
                include_docs=not no_docs,
                include_pre_commit=not no_pre_commit,
                include_github_actions=github_actions,
                use_async=async_support,
            )

            output_path = Path(output_dir) if output_dir else Path.cwd() / project_name
            confirmed = True
        else:
            # Interactive mode
            if project_name:
                console.print(f"Creating project: [green]{project_name}[/green]")

            config = collect_project_config()

            # Override with provided values
            if project_name:
                config.name = project_name
            if author:
                config.author = author
            if email:
                config.email = email

            # Get output directory
            output_path = (
                Path(output_dir) if output_dir
                else get_output_directory(config.name)
            )

            # Confirm creation
            confirmed = confirm_project_creation(config, output_path)

        if not confirmed:
            console.print("❌ Project creation cancelled")
            raise typer.Exit(0)

        # Create project
        template_context = {
            "project_name": config.name,
            "project_description": config.description,
            "author_name": config.author,
            "author_email": config.email,
            "python_version": config.python_version,
            "package_name": config.name.replace("-", "_"),
            "include_tests": config.include_tests,
            "include_docs": config.include_docs,
            "include_pre_commit": config.include_pre_commit,
            "include_github_actions": config.include_github_actions,
            "use_async": config.use_async,
        }

        create_project_structure(output_path, template, template_context)

        if not yes:
            show_next_steps(output_path, config.name)
        else:
            console.print(f"✅ Project created at {output_path}")

    except KeyboardInterrupt:
        console.print("\n❌ Operation cancelled by user")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    from kens_python_cli import __version__
    console.print(f"kens-python-cli version [green]{__version__}[/green]")


@app.command()
def list_templates() -> None:
    """List available templates."""
    from kens_python_cli.utils.file_ops import get_template_path

    templates = ["default"]  # TODO: Add more templates

    console.print("📋 [bold blue]Available Templates[/bold blue]\n")

    for template in templates:
        try:
            template_path = get_template_path(template)
            console.print(f"  • [green]{template}[/green] - Modern Python CLI template")
        except ValueError:
            console.print(f"  • [red]{template}[/red] - Template not found")


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
