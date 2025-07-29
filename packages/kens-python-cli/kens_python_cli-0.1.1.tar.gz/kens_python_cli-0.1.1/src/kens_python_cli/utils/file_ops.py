"""Cross-platform file operations utilities."""

import shutil
import stat
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def ensure_directory_exists(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def copy_file_with_template(
    source: Path,
    destination: Path,
    context: Optional[Dict[str, Any]] = None,
    make_executable: bool = False,
) -> None:
    """Copy file with optional template rendering."""
    ensure_directory_exists(destination.parent)

    if context and source.suffix in {".py", ".toml", ".md", ".txt", ".yml", ".yaml"}:
        # Render template
        template = Template(source.read_text(encoding="utf-8"))
        content = template.render(**context)
        destination.write_text(content, encoding="utf-8")
    else:
        # Direct copy for binary files or when no context
        shutil.copy2(source, destination)

    if make_executable:
        # Make file executable (cross-platform)
        current_mode = destination.stat().st_mode
        destination.chmod(current_mode | stat.S_IEXEC)


def copy_template_directory(
    source_dir: Path,
    destination_dir: Path,
    context: Optional[Dict[str, Any]] = None,
    ignore_patterns: Optional[list[str]] = None,
) -> None:
    """Copy entire template directory with context substitution."""
    ignore_patterns = ignore_patterns or []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Copying template files...", total=None)

        for source_path in source_dir.rglob("*"):
            if source_path.is_file():
                # Skip ignored patterns
                if any(pattern in str(source_path) for pattern in ignore_patterns):
                    continue

                # Calculate relative path and destination
                relative_path = source_path.relative_to(source_dir)
                destination_path = destination_dir / relative_path

                # Render template names if they contain template variables
                if context:
                    relative_str = str(relative_path)
                    if "{{" in relative_str:
                        template = Template(relative_str)
                        relative_str = template.render(**context)
                        destination_path = destination_dir / relative_str

                # Copy file with template rendering
                copy_file_with_template(
                    source_path,
                    destination_path,
                    context,
                    make_executable=source_path.suffix == ".sh",
                )


def validate_project_path(path: Path) -> None:
    """Validate that project path is suitable for new project."""
    if path.exists():
        if path.is_file():
            raise ValueError(f"Path {path} is a file, not a directory")

        if any(path.iterdir()):
            raise ValueError(f"Directory {path} is not empty")


def get_template_path(template_name: str) -> Path:
    """Get path to template directory."""
    package_dir = Path(__file__).parent.parent
    templates_dir = package_dir / "templates"
    template_path = templates_dir / template_name

    if not template_path.exists():
        raise ValueError(f"Template '{template_name}' not found")

    return template_path


def render_template_string(template_str: str, context: Dict[str, Any]) -> str:
    """Render a template string with context."""
    template = Template(template_str)
    return template.render(**context)


def setup_jinja_environment(templates_dir: Path) -> Environment:
    """Setup Jinja2 environment for template rendering."""
    return Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def create_project_structure(
    project_path: Path,
    template_name: str,
    context: Dict[str, Any],
) -> None:
    """Create complete project structure from template."""
    template_path = get_template_path(template_name)

    # Validate destination
    validate_project_path(project_path)

    # Copy template with context
    copy_template_directory(
        template_path,
        project_path,
        context,
        ignore_patterns=[".git", "__pycache__", ".pytest_cache", ".mypy_cache"],
    )

    console.print(f"✅ Created project at {project_path}")

