# Hey Claude! Your New Python CLI Developer Guide 🐍

I'm working with someone who's **new to Python CLI development** and chose this modern stack to learn with you. Please be extra helpful, explain concepts clearly, and guide them through building their first real Python CLI application.

## 🏗️ What You're Looking At

This is a **modern Python CLI project** created with `kens-python-cli`. It's designed to be:
- **Beginner-friendly** but production-ready
- **Type-safe** with full mypy support
- **Well-tested** with pytest
- **Beautiful** with Rich terminal output
- **Cross-platform** (Windows, macOS, Linux)

## 🛠️ The Tech Stack (2025 Edition)

### Core Framework
- **[Typer](https://typer.tiangolo.com/)** - The "FastAPI of CLIs" - modern, type-safe CLI framework
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal output, progress bars, tables
- **[Pydantic](https://pydantic.dev/)** - Data validation and settings management

### Development Tools
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast Python package manager (replaces pip/poetry)
- **[Ruff](https://github.com/astral-sh/ruff)** - All-in-one linter and formatter (replaces Black, isort, flake8)
- **[mypy](https://mypy.readthedocs.io/)** - Static type checking
- **[pytest](https://pytest.org/)** - Modern testing framework

### Why This Stack?
- **Typer** is used by companies like Netflix, Uber, and Microsoft for internal tools
- **Rich** makes your CLI look professional and user-friendly
- **uv** is 10-100x faster than pip and handles dependencies better
- **Ruff** combines multiple tools into one blazing-fast linter

## 📁 Project Structure (Think of it as a House)

```
{{ project_name }}/
├── src/{{ package_name }}/        # 🏠 Main house (your code lives here)
│   ├── __init__.py               # 📋 House nameplate
│   ├── main.py                   # 🚪 Front door (CLI entry point)
│   ├── config.py                 # ⚙️ House settings
│   ├── commands/                 # 🏠 Rooms (different CLI commands)
│   │   ├── info.py              # 📊 Information room
│   │   └── process.py           # 🔄 Processing room
│   └── utils/                    # 🧰 Toolshed (helper functions)
│       ├── logging.py           # 📝 Logging utilities
│       └── helpers.py           # 🔧 General helpers
{% if include_tests %}├── tests/                       # 🧪 Quality control lab
│   ├── test_main.py            # 🧪 Test the main functionality
│   └── conftest.py             # 🧪 Test configuration
{% endif %}├── pyproject.toml               # 📄 House blueprint (project config)
└── README.md                    # 📖 House manual
```

## 🚀 Getting Started

### 1. First Time Setup
```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --dev

{% if include_pre_commit %}# Install pre-commit hooks (quality checks)
uv run pre-commit install
{% endif %}
```

### 2. Try Your CLI
```bash
# Run your CLI
uv run {{ project_name.replace('-', '_') }} --help

# Try the hello command
uv run {{ project_name.replace('-', '_') }} hello --name "Claude"

# Check system info
uv run {{ project_name.replace('-', '_') }} info system
```

### 3. Make Changes
```bash
# Edit src/{{ package_name }}/main.py to add new commands
# Edit src/{{ package_name }}/commands/ to add new functionality

# Format your code
uv run ruff format

# Check for issues
uv run ruff check

# Run type checking
uv run mypy src/{{ package_name }}
{% if include_tests %}
# Run tests
uv run pytest
{% endif %}
```

## 🧭 Development Workflow

### Adding a New Command
1. Create a new file in `src/{{ package_name }}/commands/` (e.g., `hello.py`)
2. Import it in `src/{{ package_name }}/main.py`
3. Add it to the main app with `app.add_typer(hello.app, name="hello")`

### Example New Command
```python
# src/{{ package_name }}/commands/hello.py
import typer
from rich.console import Console

app = typer.Typer(help="Greeting commands")
console = Console()

@app.command()
def world(name: str = "World") -> None:
    """Say hello to the world."""
    console.print(f"Hello, {name}! 🌍")
```

## 🎨 Making It Beautiful with Rich

### Progress Bars
```python
from rich.progress import Progress, SpinnerColumn, TextColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
) as progress:
    task = progress.add_task("Processing files...", total=100)
    # Your processing code here
    progress.advance(task)
```

### Tables
```python
from rich.table import Table

table = Table(title="Results")
table.add_column("Name", style="cyan")
table.add_column("Value", justify="right")
table.add_row("Items", "42")
console.print(table)
```

### Colors and Styling
```python
console.print("✅ [green]Success![/green]")
console.print("❌ [red]Error occurred[/red]")
console.print("⚠️  [yellow]Warning message[/yellow]")
```

## 📋 Common Patterns

### Command with Options
```python
@app.command()
def process(
    input_file: Path = typer.Argument(..., help="Input file"),
    output_dir: Path = typer.Option(Path.cwd(), help="Output directory"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Process a file."""
    if verbose:
        console.print(f"Processing {input_file} -> {output_dir}")
```

### Configuration Management
```python
from {{ package_name }}.config import get_config

config = get_config()
if config.debug:
    console.print("[dim]Debug mode enabled[/dim]")
```

### Error Handling
```python
try:
    # Your code here
    pass
except FileNotFoundError:
    console.print("[red]File not found![/red]")
    raise typer.Exit(1)
```

## 🧪 Testing Your CLI

{% if include_tests %}### Running Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov={{ package_name }}

# Run specific test
uv run pytest tests/test_main.py::test_hello_command
```

### Writing Tests
```python
def test_hello_command():
    """Test the hello command."""
    from {{ package_name }}.main import app
    from typer.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(app, ["hello", "--name", "Test"])

    assert result.exit_code == 0
    assert "Hello, Test!" in result.stdout
```
{% else %}### Testing Setup
Add `pytest` to your dependencies and create a `tests/` directory to start testing your CLI.
{% endif %}

## 🔧 Common CLI Patterns

### File Processing
```python
def process_files(files: List[Path]) -> None:
    """Process multiple files with progress."""
    with Progress() as progress:
        task = progress.add_task("Processing...", total=len(files))

        for file in files:
            # Process each file
            progress.advance(task)
```

### Configuration Files
```python
# Use platformdirs for cross-platform config
import platformdirs
config_dir = Path(platformdirs.user_config_dir("{{ project_name }}"))
config_file = config_dir / "config.toml"
```

### Interactive Prompts
```python
from rich.prompt import Prompt, Confirm

name = Prompt.ask("What's your name?")
proceed = Confirm.ask("Continue?", default=True)
```

## 📚 Learning Resources

### Python CLI Development
- [Typer Documentation](https://typer.tiangolo.com/) - Your CLI framework
- [Rich Documentation](https://rich.readthedocs.io/) - Beautiful terminal output
- [Click Documentation](https://click.palletsprojects.com/) - Typer is built on Click

### Python Best Practices
- [Real Python CLI Articles](https://realpython.com/python-click/) - Comprehensive guides
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Type safety
- [pathlib Guide](https://docs.python.org/3/library/pathlib.html) - Modern path handling

## 🤖 Working with Claude

### How to Get Help
1. **Be specific**: "How do I add a command that processes CSV files?"
2. **Show context**: Share the relevant code files
3. **Ask for examples**: "Can you show me how to add a progress bar?"
4. **Request explanations**: "Why do we use Typer instead of argparse?"

### Good Questions to Ask
- "How do I add input validation to my CLI?"
- "What's the best way to handle configuration files?"
- "How do I make my CLI work on Windows and macOS?"
- "Can you help me add tests for my new command?"

## 📈 Next Steps

### Beginner Level
1. Add a new command to the CLI
2. Implement file reading/writing
3. Add configuration options
4. Create interactive prompts

### Intermediate Level
1. Add comprehensive error handling
2. Implement logging
3. Add progress bars for long operations
4. Create subcommands with groups

### Advanced Level
1. Add plugin system
2. Implement caching
3. Add async support for I/O operations
4. Create installable packages

## 🚀 Publishing Your CLI

When you're ready to share your CLI:

```bash
# Build the package
uv build

# Test installation
uv pip install dist/*.whl

# Publish to PyPI (when ready)
uv publish
```

Users can then install with: `uvx {{ project_name }} my-command`

---

## 🎯 Remember

- **Start simple**: Begin with basic commands and add complexity gradually
- **Use types**: Python type hints make your code self-documenting
- **Test early**: Add tests as you build features
- **Make it beautiful**: Rich makes your CLI stand out
- **Ask for help**: Claude is here to guide you through every step!

**Happy coding! 🚀**

*This project was created with [kens-python-cli](https://github.com/ken/kens-python-cli) - the modern Python CLI scaffolding tool.*
