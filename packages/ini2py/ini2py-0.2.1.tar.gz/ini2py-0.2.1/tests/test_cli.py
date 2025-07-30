import configparser
import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from ini2py.cli import (
    generate_schema_class,
    infer_type,
    main,
    run_generator,
    snake_to_camel,
)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_snake_to_camel(self):
        """Test snake_case to CamelCase conversion."""
        assert snake_to_camel("test_section") == "TestSection"
        assert snake_to_camel("api_key") == "ApiKey"
        assert snake_to_camel("simple") == "Simple"
        assert snake_to_camel("multi_word_test") == "MultiWordTest"

    def test_infer_type(self):
        """Test type inference from string values."""
        assert infer_type("123") == "int"
        assert infer_type("123.45") == "float"
        assert infer_type("true") == "boolean"
        assert infer_type("True") == "boolean"
        assert infer_type("false") == "boolean"
        assert infer_type("False") == "boolean"
        assert infer_type("hello") == "str"
        assert infer_type("") == "str"


class TestSchemaGeneration:
    """Test schema class generation."""

    def test_generate_schema_class(self):
        """Test generation of schema class code."""
        # Create a mock config section
        config = configparser.ConfigParser()
        config.add_section("database")
        config.set("database", "host", "localhost")
        config.set("database", "port", "5432")
        config.set("database", "debug", "true")
        config.set("database", "timeout", "30.5")

        section = config["database"]
        result = generate_schema_class("database", section)

        # Check if class is properly named
        assert "class DatabaseSchema(ConfigSchema):" in result
        assert '"""[database]"""' in result

        # Check if properties are generated correctly
        assert "@property" in result
        assert "def host(self):" in result
        assert "def port(self):" in result
        assert "def debug(self):" in result
        assert "def timeout(self):" in result

        # Check if correct getter methods are used
        assert "getint('port')" in result
        assert "getboolean('debug')" in result
        assert "getfloat('timeout')" in result
        assert "get('host')" in result


class TestCLI:
    """Test CLI functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()

        # Create a sample config.ini
        self.config_content = """[system]
mode = development
debug = true
port = 8080
timeout = 30.5

[database]
host = localhost
port = 5432
user = admin
password = secret123

[redis]
host = 127.0.0.1
port = 6379
db = 0

[api]
key = sk-1234567890abcdef
model = gpt-4
temperature = 0.7
"""

        self.config_path = os.path.join(self.temp_dir, "config.ini")
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(self.config_content)

    def teardown_method(self):
        """Clean up after each test."""
        shutil.rmtree(self.temp_dir)

    def test_cli_with_explicit_paths(self):
        """Test CLI with explicit config and output paths."""
        output_dir = os.path.join(self.temp_dir, "output")

        result = self.runner.invoke(
            main, ["--config", self.config_path, "--output", output_dir]
        )

        assert result.exit_code == 0
        assert "Successfully generated" in result.output

        # Check if files were created
        schema_path = os.path.join(output_dir, "schema.py")
        manager_path = os.path.join(output_dir, "manager.py")

        assert os.path.exists(schema_path)
        assert os.path.exists(manager_path)

        # Check schema.py content
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_content = f.read()
            assert "class SystemSchema(ConfigSchema):" in schema_content
            assert "class DatabaseSchema(ConfigSchema):" in schema_content
            assert "class RedisSchema(ConfigSchema):" in schema_content
            assert "class ApiSchema(ConfigSchema):" in schema_content

        # Check manager.py content
        with open(manager_path, "r", encoding="utf-8") as f:
            manager_content = f.read()
            assert "SystemSchema," in manager_content
            assert "DatabaseSchema," in manager_content
            assert "self.system = SystemSchema" in manager_content
            assert "self.database = DatabaseSchema" in manager_content

    def test_cli_interactive_mode(self):
        """Test CLI in interactive mode."""
        output_dir = os.path.join(self.temp_dir, "output")

        # Simulate user input
        result = self.runner.invoke(main, input=f"{self.config_path}\n{output_dir}\n")

        assert result.exit_code == 0
        assert "Successfully generated" in result.output

        # Check if files were created
        assert os.path.exists(os.path.join(output_dir, "schema.py"))
        assert os.path.exists(os.path.join(output_dir, "manager.py"))

    def test_cli_with_nonexistent_config(self):
        """Test CLI with non-existent config file."""
        fake_config = os.path.join(self.temp_dir, "nonexistent.ini")
        output_dir = os.path.join(self.temp_dir, "output")

        result = self.runner.invoke(
            main, ["--config", fake_config, "--output", output_dir]
        )

        # Should fail because file doesn't exist
        assert result.exit_code != 0

    def test_run_generator_function(self):
        """Test the run_generator function directly."""
        output_dir = os.path.join(self.temp_dir, "direct_output")

        # This should work without raising exceptions
        run_generator(self.config_path, output_dir)

        # Check if files were created
        assert os.path.exists(os.path.join(output_dir, "schema.py"))
        assert os.path.exists(os.path.join(output_dir, "manager.py"))


class TestGeneratedCode:
    """Test the functionality of generated code."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.temp_dir = tempfile.mkdtemp()

        # Create config.ini
        config_content = """[database]
host = localhost
port = 5432
debug = true
timeout = 30.5
password = secret123

[redis]
host = 127.0.0.1
port = 6379
db = 0
"""

        self.config_path = os.path.join(self.temp_dir, "config.ini")
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        # Generate the schema files
        self.output_dir = os.path.join(self.temp_dir, "generated")
        run_generator(self.config_path, self.output_dir)

    def teardown_method(self):
        """Clean up after each test."""
        shutil.rmtree(self.temp_dir)

    def test_generated_schema_structure(self):
        """Test that generated schema has correct structure."""
        schema_path = os.path.join(self.output_dir, "schema.py")

        with open(schema_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for required imports and base class
        assert "from configparser import SectionProxy" in content
        assert "class ConfigSchema:" in content

        # Check for generated classes
        assert "class DatabaseSchema(ConfigSchema):" in content
        assert "class RedisSchema(ConfigSchema):" in content

        # Check for properties
        assert "@property" in content
        assert "def host(self):" in content
        assert "def port(self):" in content

        # Check for proper getter methods
        assert "getint(" in content
        assert "getboolean(" in content
        assert "getfloat(" in content
        assert "get(" in content

    def test_generated_manager_structure(self):
        """Test that generated manager has correct structure."""
        manager_path = os.path.join(self.output_dir, "manager.py")

        with open(manager_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for required imports
        assert "import configparser" in content
        assert "from watchdog.observers import Observer" in content
        assert "from .schema import" in content

        # Check for manager class and methods
        assert "class ConfigManager(object):" in content
        assert "def __init__(self," in content
        assert "def reload_config(self):" in content
        assert "def _start_watchdog(self):" in content

        # Check for generated properties
        assert "self.database = DatabaseSchema" in content
        assert "self.redis = RedisSchema" in content


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_config_file(self):
        """Test handling of empty config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("")  # Empty file
            empty_config_path = f.name

        try:
            temp_output = tempfile.mkdtemp()

            # Should not crash, but might not generate useful classes
            run_generator(empty_config_path, temp_output)

            # Files should still be created
            assert os.path.exists(os.path.join(temp_output, "schema.py"))
            assert os.path.exists(os.path.join(temp_output, "manager.py"))

        finally:
            os.unlink(empty_config_path)
            shutil.rmtree(temp_output)

    def test_config_with_special_characters(self):
        """Test handling of config with special characters in values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(
                """[special]
url = https://example.com/api?key=value&other=test
message = Hello, World! This has "quotes" and 'apostrophes'
path = /path/to/file with spaces
"""
            )
            special_config_path = f.name

        try:
            temp_output = tempfile.mkdtemp()

            # Should handle special characters gracefully
            run_generator(special_config_path, temp_output)

            assert os.path.exists(os.path.join(temp_output, "schema.py"))
            assert os.path.exists(os.path.join(temp_output, "manager.py"))

        finally:
            os.unlink(special_config_path)
            shutil.rmtree(temp_output)


if __name__ == "__main__":
    pytest.main([__file__])
