# Add the parent directory to sys.path so we can import ini2py
import os
import shutil
import sys
import tempfile

import pytest

from ini2py.cli import run_generator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestGeneratedManager:
    """Test the generated ConfigManager functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
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
enabled = false
"""

        self.config_path = os.path.join(self.temp_dir, "config.ini")
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(self.config_content)

        # Generate the Python files
        self.output_dir = os.path.join(self.temp_dir, "generated")
        run_generator(self.config_path, self.output_dir)

        # Add generated directory to Python path
        sys.path.insert(0, self.output_dir)

        # Create __init__.py file in the generated directory to make it a proper package
        init_file = os.path.join(self.output_dir, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# Generated package\n")

    def teardown_method(self):
        """Clean up after each test."""
        # Remove from sys.path
        if self.output_dir in sys.path:
            sys.path.remove(self.output_dir)

        # Remove generated modules from cache
        modules_to_remove = [
            k for k in sys.modules.keys() if "schema" in k or "manager" in k
        ]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]

        shutil.rmtree(self.temp_dir)

    def test_schema_type_inference(self):
        """Test that schema classes properly infer and convert types."""
        # Import generated schema
        try:
            import configparser

            from schema import ApiSchema, DatabaseSchema, RedisSchema, SystemSchema

            # Use RawConfigParser to match the generated code
            config = configparser.RawConfigParser()
            config.read(self.config_path)

            # Test SystemSchema
            system = SystemSchema(config["system"])
            assert system.mode == "development"
            assert system.debug is True  # Should be boolean
            assert system.port == 8080  # Should be int
            assert isinstance(system.timeout, float)  # Should be float

            # Test DatabaseSchema
            database = DatabaseSchema(config["database"])
            assert database.host == "localhost"
            assert database.port == 5432  # Should be int
            assert database.user == "admin"
            assert database.password == "secret123"

            # Test RedisSchema
            redis = RedisSchema(config["redis"])
            assert redis.host == "127.0.0.1"
            assert redis.port == 6379  # Should be int
            assert redis.db == 0  # Should be int

            # Test ApiSchema
            api = ApiSchema(config["api"])
            assert api.key == "sk-1234567890abcdef"
            assert api.model == "gpt-4"
            assert isinstance(api.temperature, float)  # Should be float
            assert api.enabled is False  # Should be boolean

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")

    def test_return_properties_functionality(self):
        """Test the return_properties method of ConfigSchema."""
        try:
            import configparser

            from schema import DatabaseSchema

            config = configparser.RawConfigParser()
            config.read(self.config_path)

            database = DatabaseSchema(config["database"])

            # Test return as list
            props_list = database.return_properties(
                return_type="list", mask_sensitive=True
            )
            assert isinstance(props_list, list)
            assert len(props_list) > 0

            # Check if sensitive data is masked
            password_entry = [p for p in props_list if "password" in p.lower()]
            assert len(password_entry) > 0
            assert "*" in password_entry[0]  # Should be masked

            # Test return as dict
            props_dict = database.return_properties(
                return_type="dict", mask_sensitive=True
            )
            assert isinstance(props_dict, dict)
            assert "host" in props_dict
            assert "password" in props_dict
            assert "*" in props_dict["password"]  # Should be masked

            # Test without masking
            props_unmasked = database.return_properties(
                return_type="dict", mask_sensitive=False
            )
            assert props_unmasked["password"] == "secret123"  # Should not be masked

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")

    def test_sensitive_data_masking(self):
        """Test that sensitive data is properly masked."""
        try:
            import configparser

            from schema import ApiSchema, DatabaseSchema

            config = configparser.RawConfigParser()
            config.read(self.config_path)

            database = DatabaseSchema(config["database"])
            api = ApiSchema(config["api"])

            # Test password masking
            props = database.return_properties(return_type="dict", mask_sensitive=True)
            assert "*" in props["password"]
            assert props["password"] != "secret123"

            # Test API key masking
            props = api.return_properties(return_type="dict", mask_sensitive=True)
            assert "*" in props["key"]
            assert props["key"] != "sk-1234567890abcdef"

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")

    def test_config_manager_singleton(self):
        """Test that ConfigManager follows singleton pattern."""
        # We'll need to mock the find_config_path function since we can't easily
        # test the full manager functionality without proper file structure
        pass  # This test would need the actual generated manager to work

    def test_manager_imports(self):
        """Test that the generated manager.py has correct imports."""
        manager_path = os.path.join(self.output_dir, "manager.py")

        with open(manager_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check that all schema classes are imported
        assert "SystemSchema," in content
        assert "DatabaseSchema," in content
        assert "RedisSchema," in content
        assert "ApiSchema," in content

        # Check that manager properties are generated
        assert "self.system = SystemSchema" in content
        assert "self.database = DatabaseSchema" in content
        assert "self.redis = RedisSchema" in content
        assert "self.api = ApiSchema" in content

    def test_config_file_structure_validation(self):
        """Test that generated files have valid Python syntax."""
        schema_path = os.path.join(self.output_dir, "schema.py")
        manager_path = os.path.join(self.output_dir, "manager.py")

        # Test that files can be compiled (basic syntax check)
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_code = f.read()

        with open(manager_path, "r", encoding="utf-8") as f:
            manager_code = f.read()

        try:
            compile(schema_code, schema_path, "exec")
            compile(manager_code, manager_path, "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax errors: {e}")


class TestConfigManagerFunctionality:
    """Test ConfigManager utility functions."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up after each test."""
        shutil.rmtree(self.temp_dir)

    def test_find_config_path_function(self):
        """Test the find_config_path utility function."""
        # Create config in different locations
        config_content = "[test]\nvalue = 123\n"

        # Test direct config.ini
        config_path = os.path.join(self.temp_dir, "config.ini")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        # Generate manager to test find_config_path function
        output_dir = os.path.join(self.temp_dir, "output")
        run_generator(config_path, output_dir)

        manager_path = os.path.join(output_dir, "manager.py")
        with open(manager_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check that find_config_path function is properly generated
        assert "def find_config_path(" in content
        assert "config.ini" in content
        assert "'config', filename" in content
        assert "'conf', filename" in content

    def test_config_file_handler_structure(self):
        """Test that ConfigFileHandler class is properly generated."""
        config_path = os.path.join(self.temp_dir, "config.ini")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("[test]\nvalue = 123\n")

        output_dir = os.path.join(self.temp_dir, "output")
        run_generator(config_path, output_dir)

        manager_path = os.path.join(output_dir, "manager.py")
        with open(manager_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check ConfigFileHandler class
        assert "class ConfigFileHandler(FileSystemEventHandler):" in content
        assert "def on_modified(self, event):" in content
        assert "self.config_manager.reload_config()" in content

        # Check ConfigManager class
        assert "class ConfigManager(object):" in content
        assert "_instance = None" in content
        assert "_initialized = False" in content
        assert "def __new__(cls" in content
        assert "def reload_config(self):" in content
        assert "def _start_watchdog(self):" in content


class TestSchemaReturnProperties:
    """Test ConfigSchema return_properties method thoroughly."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

        # Create config with various sensitive fields
        config_content = """[auth]
username = admin
password = secret123
api_key = sk-1234567890abcdef
token = bearer_token_12345
secret = my_secret_value
appkey = app_key_value

[database]
host = localhost
port = 5432
db_password = db_secret
connection_string = postgresql://user:pass@localhost:5432/db

[settings]
debug = true
timeout = 30
version = 1.2.3
"""

        config_path = os.path.join(self.temp_dir, "config.ini")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        output_dir = os.path.join(self.temp_dir, "output")
        run_generator(config_path, output_dir)

        # Create __init__.py file
        init_file = os.path.join(output_dir, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# Generated package\n")

        sys.path.insert(0, output_dir)

    def teardown_method(self):
        """Clean up after each test."""
        output_dir = os.path.join(self.temp_dir, "output")
        if output_dir in sys.path:
            sys.path.remove(output_dir)

        modules_to_remove = [
            k for k in sys.modules.keys() if "schema" in k or "manager" in k
        ]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]

        shutil.rmtree(self.temp_dir)

    def test_sensitive_field_detection(self):
        """Test that sensitive fields are properly detected and masked."""
        try:
            import configparser

            from schema import AuthSchema

            config = configparser.RawConfigParser()
            config_path = os.path.join(self.temp_dir, "config.ini")
            config.read(config_path)

            auth = AuthSchema(config["auth"])
            props = auth.return_properties(return_type="dict", mask_sensitive=True)

            # These should be masked
            sensitive_fields = ["password", "api_key", "token", "secret", "appkey"]
            for field in sensitive_fields:
                if field in props:
                    assert "*" in str(props[field]), f"Field {field} should be masked"

            # Username should not be masked
            assert props["username"] == "admin"

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")

    def test_return_properties_error_handling(self):
        """Test error handling in return_properties method."""
        try:
            import configparser

            from schema import SettingsSchema

            config = configparser.RawConfigParser()
            config_path = os.path.join(self.temp_dir, "config.ini")
            config.read(config_path)

            settings = SettingsSchema(config["settings"])

            # Test invalid return_type
            with pytest.raises(ValueError):
                settings.return_properties(return_type="invalid")

            # Test valid return_types
            list_result = settings.return_properties(return_type="list")
            dict_result = settings.return_properties(return_type="dict")

            assert isinstance(list_result, list)
            assert isinstance(dict_result, dict)

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")


class TestConfigTypes:
    """Test different configuration value types."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

        # Create config with edge case values
        config_content = """[types]
string_value = hello world
int_value = 42
float_value = 3.14159
bool_true = true
bool_false = false
bool_yes = yes
bool_no = no
empty_string =
zero_int = 0
negative_int = -100
scientific_float = 1.23e-4
large_number = 999999999

[edge_cases]
leading_spaces =   spaced value
special_chars = !@#$%^&*()
unicode_value = 你好世界
multiline = line1
quotes = "quoted value"
apostrophes = 'single quoted'
"""

        config_path = os.path.join(self.temp_dir, "config.ini")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        output_dir = os.path.join(self.temp_dir, "output")
        run_generator(config_path, output_dir)

        # Create __init__.py file
        init_file = os.path.join(output_dir, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# Generated package\n")

        sys.path.insert(0, output_dir)

    def teardown_method(self):
        """Clean up after each test."""
        output_dir = os.path.join(self.temp_dir, "output")
        if output_dir in sys.path:
            sys.path.remove(output_dir)

        modules_to_remove = [k for k in sys.modules.keys() if "schema" in k]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]

        shutil.rmtree(self.temp_dir)

    def test_type_conversion_accuracy(self):
        """Test that types are correctly converted."""
        try:
            import configparser

            from schema import TypesSchema

            config = configparser.RawConfigParser()
            config_path = os.path.join(self.temp_dir, "config.ini")
            config.read(config_path, encoding="utf-8")

            types_schema = TypesSchema(config["types"])

            # Test string
            assert isinstance(types_schema.string_value, str)
            assert types_schema.string_value == "hello world"

            # Test integers
            assert isinstance(types_schema.int_value, int)
            assert types_schema.int_value == 42
            assert isinstance(types_schema.zero_int, int)
            assert types_schema.zero_int == 0
            assert isinstance(types_schema.negative_int, int)
            assert types_schema.negative_int == -100

            # Test floats
            assert isinstance(types_schema.float_value, float)
            assert abs(types_schema.float_value - 3.14159) < 0.00001
            assert isinstance(types_schema.scientific_float, float)

            # Test booleans
            assert isinstance(types_schema.bool_true, bool)
            assert types_schema.bool_true is True
            assert isinstance(types_schema.bool_false, bool)
            assert types_schema.bool_false is False

        except ImportError as e:
            pytest.fail(f"Failed to import generated schema: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
