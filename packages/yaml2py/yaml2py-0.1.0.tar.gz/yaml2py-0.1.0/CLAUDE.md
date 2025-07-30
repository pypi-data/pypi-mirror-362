# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

yaml2py is a CLI tool that generates type-hinted Python config classes from YAML files. It automatically infers types, supports hot reloading, and provides secure handling of sensitive configuration data.

## Key Commands

### Development Setup
```bash
# Install in development mode with all dependencies
make install-dev
# or
pip install -e .[dev]

# Complete dev environment setup
make dev-setup
```

### Testing
```bash
# Run all tests
make test
# or
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_cli.py

# Run tests with coverage
make test-coverage

# Run tests with specific marker
python -m pytest -m "not slow"  # Skip slow tests
python -m pytest -m cli         # Only CLI tests
```

### Code Quality
```bash
# Run all linting checks (flake8, mypy, isort)
make lint

# Auto-format code (black + isort)
make format

# Security checks
make security-check

# Full CI pipeline (format → lint → test → build)
make ci
```

### Building & Publishing
```bash
# Clean build artifacts
make clean

# Build distribution packages
make build

# Check distribution packages
make check-dist

# Upload to TestPyPI
make upload-test

# Upload to PyPI (requires proper credentials)
make upload

# Prepare for release (runs all checks)
make prepare-release
```

### Running Examples
```bash
# Run basic example
make run-example
```

## Architecture

### Core Components

1. **yaml2py/cli.py**: Main CLI interface using Click framework
   - Commands: generate (default command)
   - Entry points: `yaml2py` and `yml2py` (both work)
   - Handles argument parsing and validation
   - Smart auto-discovery of YAML files in common locations

2. **yaml2py/__init__.py**: Package initialization
   - Exports version information
   - Currently empty (generation logic is in cli.py)

3. **yaml2py/templates/**: Template files for code generation
   - `schema.py.tpl`: Configuration class template with base ConfigSchema class
   - `manager.py.tpl`: Singleton manager template with hot reload support

### Key Design Patterns

- **Singleton Pattern**: Generated ConfigManager ensures single config instance
- **Observer Pattern**: File watching with watchdog for hot reload
- **Template Method**: Code generation via string templates
- **Factory Pattern**: Dynamic class generation from YAML structure
- **Type Safety**: All generated classes use Python type hints

### Security Features

1. **Sensitive Data Handling**: 
   - Properties return actual values (no masking in getters)
   - `print_all()` method masks sensitive fields by default
   - `return_properties()` method supports optional masking
   - Sensitive keywords: password, pwd, api_token, token, appkey, secret, key

2. **Safe YAML Loading**: Uses `yaml.safe_load()` to prevent code injection

### Testing Strategy

Tests are organized by functionality:
- `test_cli.py`: CLI command testing
- `test_manager.py`: Config manager functionality
- Uses pytest fixtures for test data
- Test markers: slow, integration, cli, generated

## Important Implementation Details

1. **Type Inference Logic**: The system analyzes YAML values to determine Python types:
   - bool: Must check before int (isinstance order matters)
   - int: Integer values
   - float: Decimal values
   - str: String values
   - List[T]: Lists with uniform or mixed types
   - Dict[str, Any]: Dictionary values
   - Nested objects become separate Schema classes

2. **File Format Support**: 
   - Supports both `.yaml` and `.yml` extensions
   - Auto-discovers files in: config.yaml/yml, config/*.yaml/yml, settings.yaml/yml, app.yaml/yml

3. **Class Generation**:
   - Snake_case properties converted to CamelCase classes
   - Handles nested dictionaries by generating nested classes
   - Lists of objects generate item classes (removes plural 's' from property name)
   - Avoids duplicate class generation with `generated_classes` tracking

4. **Template System**: 
   - Uses string templates with `{{PLACEHOLDER}}` syntax
   - Not Jinja2 despite the .tpl extension
   - Templates include base class with utility methods

## Development Notes

- Python >=3.8 required
- Dependencies: click>=8.0, watchdog>=2.1.6, pyyaml>=6.0
- Entry points: `yaml2py` and `yml2py` (defined in pyproject.toml)
- Version: 0.1.0 (semantic versioning)
- Documentation: English (README.md) and Chinese (README.zh.md, Makefile comments)
- License: MIT