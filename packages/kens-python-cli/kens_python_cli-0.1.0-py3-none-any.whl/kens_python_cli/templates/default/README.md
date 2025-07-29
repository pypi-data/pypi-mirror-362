# {{ project_name }}

{{ project_description }}

## Installation

```bash
# Install the package
uv sync

# Or install in development mode
uv sync --dev
```

## Usage

```bash
# Run the CLI tool
uv run {{ project_name.replace('-', '_') }} --help

# Or after installation
{{ project_name.replace('-', '_') }} --help
```

## Development

### Setup

```bash
# Install dependencies
uv sync --dev

# Install pre-commit hooks{% if include_pre_commit %}
uv run pre-commit install{% endif %}
```

### Running Tests

{% if include_tests %}```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov={{ package_name }}

# Run tests in watch mode
uv run pytest --watch
```{% else %}Testing setup not included. Add pytest to dependencies if needed.{% endif %}

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/{{ package_name }}
```

### Building

```bash
# Build the package
uv build

# Install locally
uv pip install dist/*.whl
```

## Project Structure

```
{{ project_name }}/
├── src/
│   └── {{ package_name }}/
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       ├── commands/        # Command modules
│       ├── utils/           # Utility functions
│       └── config.py        # Configuration
{% if include_tests %}├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py{% endif %}
├── pyproject.toml           # Project configuration
├── README.md
{% if include_pre_commit %}├── .pre-commit-config.yaml
{% endif %}{% if include_github_actions %}├── .github/
│   └── workflows/
│       └── ci.yml
{% endif %}└── .gitignore
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

---

*This project was created with [kens-python-cli](https://github.com/ken/kens-python-cli)* 🐍✨
