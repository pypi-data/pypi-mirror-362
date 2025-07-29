"""Tests for the main CLI module."""

import pytest
from typer.testing import CliRunner

from kens_python_cli.main import app


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


def test_create_command_help(runner: CliRunner) -> None:
    """Test that the create command shows help."""
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new Python CLI project" in result.output


def test_version_command(runner: CliRunner) -> None:
    """Test the version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "kens-python-cli version" in result.output


def test_list_templates_command(runner: CliRunner) -> None:
    """Test the list-templates command."""
    result = runner.invoke(app, ["list-templates"])
    assert result.exit_code == 0
    assert "Available Templates" in result.output
    assert "default" in result.output


def test_create_with_missing_name_and_yes_flag(runner: CliRunner) -> None:
    """Test that create command fails when --yes is used without project name."""
    result = runner.invoke(app, ["create", "--yes"])
    assert result.exit_code == 1
    assert "Error: --yes requires a project name" in result.output


def test_create_dry_run_validation(runner: CliRunner, tmp_path) -> None:
    """Test create command validation without actually creating files."""
    # This tests the validation logic without creating files
    project_name = "test-cli-project"

    # Test with a non-empty directory (should work with --yes flag)
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    result = runner.invoke(app, [
        "create",
        project_name,
        "--output", str(output_dir),
        "--yes"
    ])

    # Should succeed as directory validation happens during actual creation
    assert result.exit_code == 0
