"""Tests for configuration models."""

import pytest
from pydantic import ValidationError

from kens_python_cli.models.config import ProjectConfig


def test_project_config_valid() -> None:
    """Test valid project configuration."""
    config = ProjectConfig(
        name="test-project",
        description="A test project",
        author="Test Author",
        email="test@example.com",
        python_version="3.11",
    )

    assert config.name == "test-project"
    assert config.description == "A test project"
    assert config.author == "Test Author"
    assert config.email == "test@example.com"
    assert config.python_version == "3.11"


def test_project_config_name_validation() -> None:
    """Test project name validation."""
    # Valid names
    valid_names = ["my-project", "my_project", "project123", "myproject"]

    for name in valid_names:
        config = ProjectConfig(name=name)
        assert config.name == name.replace("-", "_")

    # Invalid names
    with pytest.raises(ValidationError):
        ProjectConfig(name="")

    with pytest.raises(ValidationError):
        ProjectConfig(name="123-invalid")

    with pytest.raises(ValidationError):
        ProjectConfig(name="invalid-name!")


def test_project_config_python_version_validation() -> None:
    """Test Python version validation."""
    # Valid versions
    valid_versions = ["3.11", "3.12", "3.13"]

    for version in valid_versions:
        config = ProjectConfig(name="test", python_version=version)
        assert config.python_version == version

    # Invalid version
    with pytest.raises(ValidationError):
        ProjectConfig(name="test", python_version="3.10")


def test_project_config_defaults() -> None:
    """Test default values in project configuration."""
    config = ProjectConfig(name="test-project")

    assert config.name == "test_project"
    assert config.description == ""
    assert config.author == ""
    assert config.email == ""
    assert config.python_version == "3.11"
    assert config.include_tests is True
    assert config.include_docs is True
    assert config.include_pre_commit is True
    assert config.include_github_actions is False
    assert config.use_async is False
