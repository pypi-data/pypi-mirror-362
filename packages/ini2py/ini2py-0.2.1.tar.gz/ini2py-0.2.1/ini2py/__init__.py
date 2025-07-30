"""
ini2py - A CLI tool to generate type-hinted Python config classes from .ini 
files.

This package provides a command-line tool that converts INI configuration files
into type-hinted Python classes with automatic file watching and hot reloading.

Features:
- Auto-generate type-hinted Python classes from INI files
- Intelligent type inference (int, float, boolean, string)
- Hot reloading - automatically reload when files change
- Sensitive data masking for passwords and API keys
- Smart path detection for config files
- IDE-friendly with full autocomplete support
- Singleton pattern for configuration management

Example usage:
    $ ini2py --config config.ini --output ./src/config

    Then in your Python code:
    >>> from src.config.manager import ConfigManager
    >>> config = ConfigManager()
    >>> print(config.database.host)  # Full type hints and autocomplete!
"""

__version__ = "0.2.1"
__author__ = "JonesHong"
__email__ = "latte831104@example.com"
__license__ = "MIT"

# Re-export main CLI function for programmatic use
from .cli import (
    generate_schema_class, infer_type, main, 
    run_generator, snake_to_camel
)

__all__ = [
    "main",
    "run_generator",
    "snake_to_camel",
    "infer_type",
    "generate_schema_class",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
