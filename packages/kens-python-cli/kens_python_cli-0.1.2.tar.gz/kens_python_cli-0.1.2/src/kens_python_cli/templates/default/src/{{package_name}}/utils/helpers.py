"""Helper utilities for {{ project_name }}."""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import yaml
except ImportError:
    yaml = None

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def read_file(file_path: Union[str, Path]) -> str:
    """Read text file content."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return path.read_text(encoding="utf-8")


def write_file(file_path: Union[str, Path], content: str) -> None:
    """Write content to text file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Read JSON file."""
    content = read_file(file_path)
    try:
        return json.loads(content)  # type: ignore
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}") from e


def write_json(file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
    """Write data to JSON file."""
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    write_file(file_path, content)


def read_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Read YAML file."""
    if yaml is None:
        raise ImportError("PyYAML is required for YAML support")
    
    content = read_file(file_path)
    try:
        result = yaml.safe_load(content)
        return result if result is not None else {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {file_path}: {e}") from e


def write_yaml(file_path: Union[str, Path], data: Dict[str, Any]) -> None:
    """Write data to YAML file."""
    if yaml is None:
        raise ImportError("PyYAML is required for YAML support")
    
    content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    write_file(file_path, content)


def format_size(size_bytes: int) -> str:
    """Format byte size in human readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size_float = float(size_bytes)
    while size_float >= 1024 and i < len(size_names) - 1:
        size_float /= 1024
        i += 1

    return f"{size_float:.1f} {size_names[i]}"


def format_duration(seconds: float) -> str:
    """Format duration in human readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def confirm_action(message: str, default: bool = False) -> bool:
    """Ask user for confirmation."""
    from rich.prompt import Confirm
    return Confirm.ask(message, default=default)


def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default."""
    from rich.prompt import Prompt
    return Prompt.ask(prompt, default=default or "")


def show_progress(items: List[Any], description: str = "Processing") -> Any:
    """Show progress bar for iterable processing."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(description, total=len(items))

        for item in items:
            yield item
            progress.advance(task)


def measure_time(func_name: str = "Operation") -> Any:
    """Decorator to measure function execution time."""
    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            duration = end_time - start_time
            console.print(f"⏱️  {func_name} completed in {format_duration(duration)}")

            return result
        return wrapper
    return decorator


def safe_filename(filename: str) -> str:
    """Convert string to safe filename."""
    import re

    # Replace invalid characters with underscores
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip('. ')

    # Limit length
    if len(safe_name) > 255:
        safe_name = safe_name[:255]

    return safe_name or "unnamed"


def find_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
) -> List[Path]:
    """Find files matching pattern in directory."""
    path = Path(directory)

    if not path.exists():
        return []

    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))
