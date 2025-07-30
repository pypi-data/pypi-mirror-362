"""
yaml2py - A CLI tool to generate type-hinted Python config classes from YAML files.

This package provides a command-line tool that converts YAML configuration files
into type-hinted Python classes with automatic file watching and hot reloading.

Features:
- Auto-generate type-hinted Python classes from YAML files
- Support for nested structures and complex types
- Intelligent type inference (int, float, boolean, string, list, dict)
- Hot reloading - automatically reload when files change
- Sensitive data masking for passwords and API keys
- Smart path detection for config files
- IDE-friendly with full autocomplete support
- Singleton pattern for configuration management

Example usage:
    $ yaml2py --config config.yaml --output ./src/config

    Then in your Python code:
    >>> from src.config.manager import ConfigManager
    >>> config = ConfigManager()
    >>> print(config.database.host)  # Full type hints and autocomplete!
    >>> print(config.app.features[0].name)  # Nested structures support!
"""

__version__ = "0.1.0"
__author__ = "JonesHong"
__email__ = "latte831104@example.com"
__license__ = "MIT"

# Re-export main CLI function for programmatic use
from .cli import (YamlSchemaGenerator, infer_yaml_type, main, run_generator,
                  snake_to_camel, to_snake_case)

__all__ = [
    "main",
    "run_generator",
    "snake_to_camel",
    "to_snake_case",
    "infer_yaml_type",
    "YamlSchemaGenerator",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
