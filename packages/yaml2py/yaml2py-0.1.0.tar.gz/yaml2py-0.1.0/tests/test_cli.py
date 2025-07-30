import os
import shutil
import tempfile
from typing import Any, Dict

import pytest
import yaml
from click.testing import CliRunner

from yaml2py.cli import (YamlSchemaGenerator, infer_yaml_type, main,
                         run_generator, snake_to_camel, to_snake_case)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_snake_to_camel(self):
        """Test snake_case to CamelCase conversion."""
        assert snake_to_camel("test_section") == "TestSection"
        assert snake_to_camel("api_key") == "ApiKey"
        assert snake_to_camel("simple") == "Simple"
        assert snake_to_camel("multi_word_test") == "MultiWordTest"

    def test_to_snake_case(self):
        """Test CamelCase to snake_case conversion."""
        assert to_snake_case("TestSection") == "test_section"
        assert to_snake_case("ApiKey") == "api_key"
        assert to_snake_case("Simple") == "simple"
        assert to_snake_case("MultiWordTest") == "multi_word_test"

    def test_infer_yaml_type(self):
        """Test type inference from YAML values."""
        # Basic types
        assert infer_yaml_type(123) == "int"
        assert infer_yaml_type(123.45) == "float"
        assert infer_yaml_type(True) == "bool"
        assert infer_yaml_type(False) == "bool"
        assert infer_yaml_type("hello") == "str"
        assert infer_yaml_type(None) == "Optional[Any]"

        # List types
        assert infer_yaml_type([]) == "List[Any]"
        assert infer_yaml_type([1, 2, 3]) == "List[int]"
        assert infer_yaml_type([1.1, 2.2]) == "List[float]"
        assert infer_yaml_type([True, False]) == "List[bool]"
        assert infer_yaml_type(["a", "b"]) == "List[str]"
        assert infer_yaml_type([1, "a", True]) == "List[Union[bool, int, str]]"

        # Dict type
        assert infer_yaml_type({}) == "Dict[str, Any]"
        assert infer_yaml_type({"key": "value"}) == "Dict[str, Any]"


class TestSchemaGeneration:
    """Test schema class generation."""

    def test_generate_simple_schema(self):
        """Test generation of simple schema class."""
        generator = YamlSchemaGenerator()

        data = {"host": "localhost", "port": 5432, "debug": True, "timeout": 30.5}

        result = generator.generate_class_definition("database", data)

        assert "class DatabaseSchema(ConfigSchema):" in result
        assert "def host(self) -> str:" in result
        assert "def port(self) -> int:" in result
        assert "def debug(self) -> bool:" in result
        assert "def timeout(self) -> float:" in result

    def test_generate_nested_schema(self):
        """Test generation of nested schema classes."""
        generator = YamlSchemaGenerator()

        data = {"host": "localhost", "options": {"pool_size": 10, "timeout": 30}}

        result = generator.generate_class_definition("database", data)

        assert "class OptionsSchema(ConfigSchema):" in result
        assert "class DatabaseSchema(ConfigSchema):" in result
        assert "def options(self) -> OptionsSchema:" in result
        assert "def pool_size(self) -> int:" in result

    def test_generate_list_schema(self):
        """Test generation of list schemas."""
        generator = YamlSchemaGenerator()

        data = {
            "endpoints": [
                {"path": "/users", "method": "GET"},
                {"path": "/login", "method": "POST"},
            ]
        }

        result = generator.generate_class_definition("api", data)

        assert "class EndpointSchema(ConfigSchema):" in result
        assert "def endpoints(self) -> List[EndpointSchema]:" in result
        assert "def path(self) -> str:" in result
        assert "def method(self) -> str:" in result

    def test_sensitive_field_masking(self):
        """Test that sensitive fields are properly handled."""
        generator = YamlSchemaGenerator()

        data = {"username": "admin", "password": "secret123", "api_key": "sk-123456"}

        result = generator.generate_class_definition("auth", data)

        # Check that the properties are generated correctly
        assert "def password(self) -> str:" in result
        assert "def api_key(self) -> str:" in result
        assert "def username(self) -> str:" in result
        
        # Sensitive fields should NOT be masked in properties (masking is done in print_all method)
        assert "return self._data.get('password'" in result
        assert "return self._data.get('api_key'" in result


class TestCLI:
    """Test CLI functionality."""

    def test_cli_with_valid_yaml(self):
        """Test CLI with valid YAML input."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test YAML file
            config_path = os.path.join(tmpdir, "test.yaml")
            output_dir = os.path.join(tmpdir, "output")

            test_config = {
                "app": {"name": "TestApp", "debug": True, "port": 8080},
                "database": {"host": "localhost", "port": 5432},
            }

            with open(config_path, "w") as f:
                yaml.dump(test_config, f)

            # Run CLI
            runner = CliRunner()
            result = runner.invoke(
                main, ["--config", config_path, "--output", output_dir]
            )

            assert result.exit_code == 0
            assert os.path.exists(os.path.join(output_dir, "schema.py"))
            assert os.path.exists(os.path.join(output_dir, "manager.py"))
            assert os.path.exists(os.path.join(output_dir, "__init__.py"))

    def test_cli_with_invalid_yaml(self):
        """Test CLI with invalid YAML input."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "test.yaml")
            output_dir = os.path.join(tmpdir, "output")

            # Create a YAML that is a list at root level (not dict)
            with open(config_path, "w") as f:
                f.write("- item1\n- item2\n- item3")

            runner = CliRunner()
            result = runner.invoke(
                main, ["--config", config_path, "--output", output_dir]
            )

            assert result.exit_code == 0  # Click doesn't exit with error
            assert "Error: YAML file must contain a dictionary at the root level" in result.output

    def test_cli_with_nonexistent_file(self):
        """Test CLI with non-existent file."""
        runner = CliRunner()
        result = runner.invoke(
            main, ["--config", "nonexistent.yaml", "--output", "./output"]
        )

        assert result.exit_code != 0
        assert (
            "Error: Invalid value" in result.output or "does not exist" in result.output
        )


class TestGeneratorFunction:
    """Test the run_generator function."""

    def test_run_generator_creates_files(self):
        """Test that run_generator creates expected files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.yaml")
            output_dir = os.path.join(tmpdir, "output")

            # Create test YAML
            test_data = {
                "system": {"name": "TestSystem", "version": "1.0.0"},
                "features": [
                    {"name": "feature1", "enabled": True},
                    {"name": "feature2", "enabled": False},
                ],
            }

            with open(config_path, "w") as f:
                yaml.dump(test_data, f)

            # Run generator
            run_generator(config_path, output_dir)

            # Check files were created
            assert os.path.exists(os.path.join(output_dir, "schema.py"))
            assert os.path.exists(os.path.join(output_dir, "manager.py"))
            assert os.path.exists(os.path.join(output_dir, "__init__.py"))

            # Check schema content
            with open(os.path.join(output_dir, "schema.py"), "r") as f:
                schema_content = f.read()
                assert "class SystemSchema" in schema_content
                assert "class FeatureSchema" in schema_content
                assert "def name(self)" in schema_content
                assert "def version(self)" in schema_content
                assert "def enabled(self)" in schema_content

            # Check manager content
            with open(os.path.join(output_dir, "manager.py"), "r") as f:
                manager_content = f.read()
                assert "class ConfigManager" in manager_content
                assert "SystemSchema" in manager_content
                assert "FeatureSchema" in manager_content
                assert "def system(self)" in manager_content
                assert "def features(self)" in manager_content


if __name__ == "__main__":
    pytest.main([__file__])
