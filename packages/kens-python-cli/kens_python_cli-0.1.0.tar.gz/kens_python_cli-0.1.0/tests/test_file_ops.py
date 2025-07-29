"""Tests for file operations utilities."""

import json
from pathlib import Path

import pytest

from kens_python_cli.utils.file_ops import (
    copy_file_with_template,
    create_project_structure,
    get_template_path,
    render_template_string,
    validate_project_path,
)


def test_render_template_string() -> None:
    """Test template string rendering."""
    template = "Hello {{ name }}!"
    context = {"name": "World"}
    result = render_template_string(template, context)
    assert result == "Hello World!"


def test_validate_project_path_with_empty_dir(tmp_path: Path) -> None:
    """Test validation with empty directory."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    # Should not raise
    validate_project_path(empty_dir)


def test_validate_project_path_with_file(tmp_path: Path) -> None:
    """Test validation with file path."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")

    with pytest.raises(ValueError, match="is a file, not a directory"):
        validate_project_path(file_path)


def test_validate_project_path_with_non_empty_dir(tmp_path: Path) -> None:
    """Test validation with non-empty directory."""
    non_empty_dir = tmp_path / "non_empty"
    non_empty_dir.mkdir()
    (non_empty_dir / "file.txt").write_text("test")

    with pytest.raises(ValueError, match="is not empty"):
        validate_project_path(non_empty_dir)


def test_copy_file_with_template(tmp_path: Path) -> None:
    """Test copying file with template rendering."""
    # Create source file
    source = tmp_path / "source.txt"
    source.write_text("Hello {{ name }}!")

    # Copy with template
    destination = tmp_path / "dest.txt"
    context = {"name": "World"}

    copy_file_with_template(source, destination, context)

    assert destination.read_text() == "Hello World!"


def test_copy_file_without_template(tmp_path: Path) -> None:
    """Test copying file without template rendering."""
    # Create source file
    source = tmp_path / "source.txt"
    source.write_text("Plain text content")

    # Copy without template
    destination = tmp_path / "dest.txt"

    copy_file_with_template(source, destination)

    assert destination.read_text() == "Plain text content"


def test_get_template_path() -> None:
    """Test getting template path."""
    template_path = get_template_path("default")
    assert template_path.exists()
    assert template_path.is_dir()
    assert template_path.name == "default"


def test_get_template_path_nonexistent() -> None:
    """Test getting path for non-existent template."""
    with pytest.raises(ValueError, match="Template 'nonexistent' not found"):
        get_template_path("nonexistent")


def test_create_project_structure(tmp_path: Path) -> None:
    """Test creating project structure."""
    project_path = tmp_path / "test_project"
    context = {
        "project_name": "test-project",
        "package_name": "test_project",
        "project_description": "A test project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.11",
        "include_tests": True,
        "include_docs": True,
        "include_pre_commit": True,
        "include_github_actions": False,
        "use_async": False,
    }

    create_project_structure(project_path, "default", context)

    # Check that project was created
    assert project_path.exists()
    assert project_path.is_dir()

    # Check key files exist
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "src" / "test_project" / "__init__.py").exists()
    assert (project_path / "src" / "test_project" / "main.py").exists()

    # Check template rendering worked
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert "test-project" in pyproject_content
    assert "A test project" in pyproject_content


def test_create_project_structure_with_existing_path(tmp_path: Path) -> None:
    """Test creating project structure with existing path."""
    project_path = tmp_path / "existing"
    project_path.mkdir()
    (project_path / "file.txt").write_text("existing")

    context = {
        "project_name": "test-project",
        "package_name": "test_project",
        "project_description": "A test project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.11",
        "include_tests": True,
        "include_docs": True,
        "include_pre_commit": True,
        "include_github_actions": False,
        "use_async": False,
    }

    with pytest.raises(ValueError, match="is not empty"):
        create_project_structure(project_path, "default", context)
