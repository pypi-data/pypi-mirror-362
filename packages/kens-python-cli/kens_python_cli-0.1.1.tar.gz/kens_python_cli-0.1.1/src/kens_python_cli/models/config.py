"""Configuration models for the CLI tool."""

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ProjectConfig(BaseModel):
    """Configuration for a new Python CLI project."""

    name: str = Field(..., description="Project name")
    description: str = Field(default="", description="Project description")
    author: str = Field(default="", description="Author name")
    email: str = Field(default="", description="Author email")
    python_version: str = Field(default="3.11", description="Minimum Python version")

    # Features
    include_tests: bool = Field(default=True, description="Include pytest testing setup")
    include_docs: bool = Field(default=True, description="Include documentation")
    include_pre_commit: bool = Field(default=True, description="Include pre-commit hooks")
    include_github_actions: bool = Field(default=False, description="Include GitHub Actions")

    # Template options
    template_type: str = Field(default="cli", description="Template type")
    use_async: bool = Field(default=False, description="Use async/await patterns")

    @validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate project name format."""
        if not v:
            raise ValueError("Project name cannot be empty")

        # Convert to valid Python package name
        name = v.lower().replace("-", "_").replace(" ", "_")

        # Check if valid Python identifier
        if not name.isidentifier():
            raise ValueError(f"Invalid project name: {name}")

        return name

    @validator("python_version")
    def validate_python_version(cls, v: str) -> str:
        """Validate Python version format."""
        valid_versions = ["3.11", "3.12", "3.13"]
        if v not in valid_versions:
            raise ValueError(f"Python version must be one of: {valid_versions}")
        return v


class TemplateContext(BaseModel):
    """Context passed to template files."""

    project: ProjectConfig
    output_path: Path

    class Config:
        arbitrary_types_allowed = True


class CLIConfig(BaseModel):
    """Global CLI configuration."""

    default_author: Optional[str] = None
    default_email: Optional[str] = None
    default_python_version: str = "3.11"
    templates_dir: Optional[Path] = None

    class Config:
        arbitrary_types_allowed = True
