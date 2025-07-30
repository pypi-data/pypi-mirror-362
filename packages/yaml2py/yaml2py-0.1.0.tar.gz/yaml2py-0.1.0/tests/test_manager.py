# Add the parent directory to sys.path so we can import yaml2py
import os
import shutil
import sys
import tempfile
import time

import pytest
import yaml

from yaml2py.cli import run_generator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestGeneratedManager:
    """Test the generated ConfigManager functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.temp_dir = tempfile.mkdtemp()

        # Create a sample config.yaml
        self.config_content = {
            "system": {
                "mode": "development",
                "debug": True,
                "port": 8080,
                "timeout": 30.5,
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "user": "admin",
                "password": "secret123",
                "options": {"pool_size": 10, "retry_attempts": 3},
            },
            "redis": {"host": "127.0.0.1", "port": 6379, "db": 0},
            "api": {
                "key": "sk-1234567890abcdef",
                "model": "gpt-4",
                "temperature": 0.7,
                "enabled": False,
            },
            "features": [
                {"name": "authentication", "enabled": True, "priority": 1},
                {"name": "logging", "enabled": False, "priority": 2},
            ],
        }

        self.config_path = os.path.join(self.temp_dir, "config.yaml")
        with open(self.config_path, "w") as f:
            yaml.dump(self.config_content, f)

        # Generate the Python files
        self.output_dir = os.path.join(self.temp_dir, "output")
        run_generator(self.config_path, self.output_dir)

        # Add output directory to path so we can import the generated modules
        sys.path.insert(0, self.output_dir)

    def teardown_method(self):
        """Clean up after each test."""
        # Remove from path
        if self.output_dir in sys.path:
            sys.path.remove(self.output_dir)

        # Clean up temp directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        # Clean up imported modules
        modules_to_remove = [
            name for name in sys.modules if name.startswith(("manager", "schema"))
        ]
        for module in modules_to_remove:
            del sys.modules[module]

    def test_config_manager_singleton(self):
        """Test that ConfigManager follows singleton pattern."""
        from manager import ConfigManager

        manager1 = ConfigManager(self.config_path)
        manager2 = ConfigManager(self.config_path)

        assert manager1 is manager2

    def test_basic_type_inference(self):
        """Test that basic types are inferred correctly."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # String
        assert config.system.mode == "development"
        assert isinstance(config.system.mode, str)

        # Boolean
        assert config.system.debug is True
        assert isinstance(config.system.debug, bool)

        # Integer
        assert config.system.port == 8080
        assert isinstance(config.system.port, int)

        # Float
        assert config.system.timeout == 30.5
        assert isinstance(config.system.timeout, float)

    def test_nested_config_access(self):
        """Test accessing nested configuration values."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Access nested values
        assert config.database.host == "localhost"
        assert config.database.port == 5432
        assert config.database.options.pool_size == 10
        assert config.database.options.retry_attempts == 3

    def test_list_config_access(self):
        """Test accessing list configuration values."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Access list values
        assert len(config.features) == 2

        assert config.features[0].name == "authentication"
        assert config.features[0].enabled is True
        assert config.features[0].priority == 1

        assert config.features[1].name == "logging"
        assert config.features[1].enabled is False
        assert config.features[1].priority == 2

    def test_sensitive_data_masking(self):
        """Test that sensitive data is masked in return_properties."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Direct access should return actual values (not masked)
        assert config.database.password == "secret123"
        assert config.api.key == "sk-1234567890abcdef"
        
        # Test that return_properties masks sensitive data
        props = config.database.return_properties(return_type="dict", mask_sensitive=True)
        assert "se*****23" in str(props["password"])  # Masking pattern
        
        # Test print_all method masks by default
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        config.database.print_all()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        assert "se*****23" in output  # Password should be masked in print output

    def test_return_properties_method(self):
        """Test the return_properties method."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Test list format
        props_list = config.system.return_properties(return_type="list")
        assert isinstance(props_list, list)
        assert any("mode: development" in prop for prop in props_list)
        assert any("debug: True" in prop for prop in props_list)

        # Test dict format
        props_dict = config.system.return_properties(return_type="dict")
        assert isinstance(props_dict, dict)
        assert props_dict["mode"] == "development"
        assert props_dict["debug"] is True
        assert props_dict["port"] == 8080
        assert props_dict["timeout"] == 30.5

    @pytest.mark.skip(reason="Hot reload timing is unreliable in tests")
    def test_hot_reload(self):
        """Test hot reload functionality."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Initial value
        assert config.system.mode == "development"

        # Modify the config file
        self.config_content["system"]["mode"] = "production"
        with open(self.config_path, "w") as f:
            yaml.dump(self.config_content, f)

        # Give watchdog time to detect the change
        time.sleep(2)

        # Value should be updated
        assert config.system.mode == "production"

    def test_file_not_found_error(self):
        """Test error handling when config file doesn't exist."""
        non_existent_path = os.path.join(self.temp_dir, "non_existent.yaml")

        from manager import ConfigManager

        with pytest.raises(FileNotFoundError):
            ConfigManager(non_existent_path)

    def test_to_dict_method(self):
        """Test the to_dict method of schema classes."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Test to_dict returns correct data
        system_dict = config.system.to_dict()
        assert system_dict["mode"] == "development"
        assert system_dict["debug"] is True
        assert system_dict["port"] == 8080
        assert system_dict["timeout"] == 30.5

    def test_raw_data_access(self):
        """Test accessing raw YAML data through ConfigManager."""
        from manager import ConfigManager

        config = ConfigManager(self.config_path)

        # Test get_raw_data method
        raw_data = config.get_raw_data()
        assert isinstance(raw_data, dict)
        assert "system" in raw_data
        assert "database" in raw_data
        assert raw_data["system"]["mode"] == "development"

    def test_complex_nested_structure(self):
        """Test handling of deeply nested structures."""
        # Create a more complex config
        complex_config = {
            "app": {
                "services": {
                    "cache": {
                        "provider": "redis",
                        "settings": {"ttl": 3600, "max_entries": 1000},
                    }
                }
            }
        }

        complex_path = os.path.join(self.temp_dir, "complex.yaml")
        with open(complex_path, "w") as f:
            yaml.dump(complex_config, f)

        # Generate files for complex config
        complex_output = os.path.join(self.temp_dir, "complex_output")
        run_generator(complex_path, complex_output)

        # Import and test
        sys.path.insert(0, complex_output)
        from manager import ConfigManager as ComplexConfigManager

        config = ComplexConfigManager(complex_path)
        assert config.app.services.cache.provider == "redis"
        assert config.app.services.cache.settings.ttl == 3600
        assert config.app.services.cache.settings.max_entries == 1000


if __name__ == "__main__":
    pytest.main([__file__])
