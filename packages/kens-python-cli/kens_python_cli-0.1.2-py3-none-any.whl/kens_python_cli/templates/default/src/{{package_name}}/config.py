"""Configuration management for {{ project_name }}."""

import os
from pathlib import Path
from typing import Optional

import platformdirs
from pydantic import BaseModel, Field
from rich.console import Console

console = Console()

# Configuration directory
CONFIG_DIR = Path(platformdirs.user_config_dir("{{ project_name }}"))
CONFIG_FILE = CONFIG_DIR / "config.toml"


class Config(BaseModel):
    """Application configuration."""

    debug: bool = Field(default=False, description="Enable debug mode")
    output_format: str = Field(default="table", description="Output format (table, json, yaml)")
    config_file: Path = Field(default=CONFIG_FILE, description="Configuration file path")

    class Config:
        arbitrary_types_allowed = True


def get_config() -> Config:
    """Get current configuration."""
    config = Config()

    # Override with environment variables
    if os.getenv("{{ project_name.upper().replace('-', '_') }}_DEBUG"):
        config.debug = os.getenv("{{ project_name.upper().replace('-', '_') }}_DEBUG", "").lower() == "true"

    if os.getenv("{{ project_name.upper().replace('-', '_') }}_OUTPUT_FORMAT"):
        config.output_format = os.getenv("{{ project_name.upper().replace('-', '_') }}_OUTPUT_FORMAT", "table")

    return config


def ensure_config_dir() -> None:
    """Ensure configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_data_dir() -> Path:
    """Get application data directory."""
    data_dir = Path(platformdirs.user_data_dir("{{ project_name }}"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_cache_dir() -> Path:
    """Get application cache directory."""
    cache_dir = Path(platformdirs.user_cache_dir("{{ project_name }}"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

