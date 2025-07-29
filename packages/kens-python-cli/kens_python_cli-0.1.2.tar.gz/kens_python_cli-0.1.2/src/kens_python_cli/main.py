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

console = Console()


def create_project(
    project_name: str,
    output_dir: Optional[str] = None,
    template: str = "default",
    author: Optional[str] = None,
    email: Optional[str] = None,
    python_version: str = "3.11",
    no_tests: bool = False,
    no_docs: bool = False,
    no_pre_commit: bool = False,
    github_actions: bool = False,
    async_support: bool = False,
    yes: bool = False,
) -> None:
    """Create a new Python CLI project."""
    try:
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


def main(
    project_name: Optional[str] = typer.Argument(None, help="Name of the project to create"),
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
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
    ),
) -> None:
    """🐍 Modern Python CLI scaffolding tool for rapid development"""

    if version:
        from kens_python_cli import __version__
        console.print(f"kens-python-cli version [green]{__version__}[/green]")
        return

    if not project_name:
        console.print("🐍 [bold green]Modern Python CLI scaffolding tool[/bold green]\n")
        console.print("Usage: kens-python-cli <project-name> [options]")
        console.print("   or: kens-python-cli --help")
        console.print("   or: kens-python-cli --version")
        console.print("\nExample: kens-python-cli my-awesome-cli")
        console.print("Example: kens-python-cli my-cli --yes --author 'Your Name'")
        return

    create_project(
        project_name=project_name,
        output_dir=output_dir,
        template=template,
        author=author,
        email=email,
        python_version=python_version,
        no_tests=no_tests,
        no_docs=no_docs,
        no_pre_commit=no_pre_commit,
        github_actions=github_actions,
        async_support=async_support,
        yes=yes,
    )


def cli_main() -> None:
    """Main entry point."""
    typer.run(main)


if __name__ == "__main__":
    cli_main()
