# kens-python-cli

Modern Python CLI scaffolding tool for rapid development. Create production-ready Python CLI applications with best practices, modern tooling, and beginner-friendly guides.

## Features

- 🚀 **Modern Python CLI** - Built with Typer, Rich, and Pydantic
- 🛠️ **Best Practices** - Type hints, testing, linting, and formatting
- 🔧 **Developer Experience** - Interactive prompts, beautiful output
- 📦 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🤖 **Claude-Optimized** - Special documentation for AI-assisted development
- ⚡ **Fast Setup** - Uses uv for lightning-fast dependency management

## Installation

```bash
# Run directly (recommended)
uvx kens-python-cli my-awesome-cli

# Or install globally
uv tool install kens-python-cli
```

## Quick Start

```bash
# Create a new CLI project
uvx kens-python-cli my-cli-tool

# Navigate to project
cd my-cli-tool

# Install dependencies
uv sync

# Run your CLI
uv run my_cli_tool --help
```

## Usage

### Interactive Mode (Recommended)

```bash
uvx kens-python-cli
```

The tool will guide you through creating your CLI project with interactive prompts.

### Non-Interactive Mode

```bash
uvx kens-python-cli my-cli-tool \
  --author "Your Name" \
  --email "your@email.com" \
  --python 3.11 \
  --async \
  --github-actions \
  --yes
```

### Options

- `--author, -a` - Author name
- `--email, -e` - Author email
- `--python, -p` - Python version (3.11, 3.12, 3.13)
- `--output, -o` - Output directory
- `--template, -t` - Template to use (default: "default")
- `--async` - Use async/await patterns
- `--github-actions` - Include GitHub Actions workflow
- `--no-tests` - Skip testing setup
- `--no-docs` - Skip documentation
- `--no-pre-commit` - Skip pre-commit hooks
- `--yes, -y` - Skip interactive prompts

## What You Get

### Project Structure

```
my-cli-tool/
├── src/
│   └── my_cli_tool/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── config.py            # Configuration management
│       ├── commands/            # Command modules
│       │   ├── info.py         # System information
│       │   └── process.py      # File processing
│       └── utils/              # Utility functions
│           ├── logging.py      # Rich logging
│           └── helpers.py      # Helper functions
├── tests/                      # Comprehensive test suite
├── pyproject.toml             # Modern Python configuration
├── README.md                  # Project documentation
├── PROJECT_GUIDE.md          # Claude-optimized development guide
└── .gitignore                # Git ignore file
```

### Tech Stack

- **[Typer](https://typer.tiangolo.com/)** - Modern CLI framework
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal output
- **[Pydantic](https://pydantic.dev/)** - Data validation
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast package manager
- **[Ruff](https://github.com/astral-sh/ruff)** - Lightning-fast linter
- **[pytest](https://pytest.org/)** - Testing framework
- **[mypy](https://mypy.readthedocs.io/)** - Static type checking

### Generated Features

- ✅ **Interactive CLI** with help, version, and configuration commands
- ✅ **Type-safe** with full mypy support
- ✅ **Beautiful output** with Rich progress bars, tables, and styling
- ✅ **Cross-platform** file operations using pathlib
- ✅ **Comprehensive testing** with pytest and coverage
- ✅ **Code quality** with Ruff linting and formatting
- ✅ **Pre-commit hooks** for automated quality checks
- ✅ **Documentation** with examples and best practices
- ✅ **Claude-optimized** development guide

## Example Generated CLI

```bash
# Your generated CLI will have these commands
my-cli-tool --help
my-cli-tool hello --name "World"
my-cli-tool info system
my-cli-tool process files *.txt --recursive
my-cli-tool config --show
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/ken/kens-python-cli.git
cd kens-python-cli

# Install dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=kens_python_cli

# Run specific test file
uv run pytest tests/test_main.py
```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/kens_python_cli
```

## Publishing

This project uses uv for publishing:

```bash
# Build the package
uv build

# Publish to PyPI
uv publish
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) by Sebastian Ramirez
- Inspired by [create-next-app](https://nextjs.org/docs/api-reference/create-next-app) for web development
- Uses [Rich](https://rich.readthedocs.io/) by Will McGugan for beautiful terminal output

---

*Create amazing Python CLI tools with modern best practices and AI-assisted development!* 🐍✨
