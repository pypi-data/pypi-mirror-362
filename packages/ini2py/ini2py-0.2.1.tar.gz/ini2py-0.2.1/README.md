# ini2py

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/ini2py.svg)](https://badge.fury.io/py/ini2py)

A CLI tool to generate type-hinted Python config classes from .ini files with automatic file watching and hot reloading capabilities.

## Features

- 🔧 **Auto-generate type-hinted Python classes** from INI configuration files
- 🔍 **Intelligent type inference** (int, float, boolean, string)
- 🔄 **Hot reloading** - automatically reload configuration when files change
- 🛡️ **Sensitive data masking** - automatically hide passwords and API keys
- 🎯 **Smart path detection** - automatically find config files in common locations
- 💡 **IDE-friendly** - full autocomplete and type hints support
- 🏗️ **Singleton pattern** - ensure single configuration instance across your app

## Installation

```bash
pip install ini2py
```

## Quick Start

### 1. Create a config.ini file

```ini
[system]
mode = development
debug = true
port = 8080
timeout = 30.5

[database]
host = localhost
port = 5432
name = myapp
user = admin
password = secret123

[redis]
host = 127.0.0.1
port = 6379
db = 0

[ai_service]
api_key = sk-1234567890abcdef
model = gpt-4
temperature = 0.7
```

### 2. Generate Python config classes

Run the CLI tool in your project directory:

```bash
ini2py
```

The tool will:
- Auto-detect your `config.ini` file
- Suggest an appropriate output directory
- Generate type-hinted Python classes

Example output:
```
Path to your config.ini file [./config/config.ini]: 
Path to the output directory for generated files [./src/config]: 
Reading configuration from: ./config/config.ini
Generating schema.py...
Successfully generated ./src/config/schema.py
Generating manager.py...
Successfully generated ./src/config/manager.py

Configuration generation complete!
```

### 3. Use in your Python code

```python
from src.config.manager import ConfigManager

# Initialize configuration manager (singleton pattern)
config = ConfigManager()

# Access configuration with full type hints and autocomplete
mode = config.system.mode          # str
debug = config.system.debug        # bool
port = config.system.port          # int
timeout = config.system.timeout    # float

# Sensitive data is automatically masked when printed
api_key = config.ai_service.api_key
print(f"API Key: {api_key}")  # Output: API Key: sk-12**************ef

# Get all properties for debugging
print("Database Config:")
print(config.database.return_properties(return_type='list'))
```

## Advanced Usage

### Manual Path Specification

```bash
# Specify custom paths
ini2py --config /path/to/config.ini --output /path/to/output/
```

### Hot Reloading

The generated config manager automatically watches for file changes:

```python
import time
from src.config.manager import ConfigManager

config = ConfigManager()

# The config will automatically reload when config.ini is modified
while True:
    print(f"Current port: {config.system.port}")
    time.sleep(2)
```

### Sensitive Data Handling

Sensitive values are automatically detected and masked based on keywords:
- `password`, `pwd`
- `api_token`, `token`
- `secret`, `key`
- `appkey`

```python
# These will be masked in output
config.database.password     # "se****23"
config.ai_service.api_key   # "sk-12**************ef"

# Get unmasked values for actual use
raw_config = config.database.return_properties(mask_sensitive=False)
```

## Configuration File Discovery

ini2py automatically searches for configuration files in these locations:
1. `./config.ini`
2. `./config/config.ini`
3. `./conf/config.ini`
4. `../config.ini` (up to 5 levels up)

## Generated File Structure

```
src/config/
├── schema.py    # Type-hinted schema classes
└── manager.py   # Configuration manager with hot reloading
```

### Generated Schema Classes

Each INI section becomes a typed schema class:

```python
class SystemSchema(ConfigSchema):
    """[system]"""
    
    @property
    def mode(self) -> str:
        return self._config_section.get('mode')
    
    @property
    def debug(self) -> bool:
        return self._config_section.getboolean('debug')
    
    @property
    def port(self) -> int:
        return self._config_section.getint('port')
```

## CLI Options

```bash
ini2py --help
```

Options:
- `--config, -c`: Path to input config.ini file
- `--output, -o`: Directory for generated files
- `--help`: Show help message

## Requirements

- Python 3.8+
- click >= 8.0
- watchdog >= 2.1.6

## Development

### Setup Development Environment

```bash
git clone https://github.com/joneshong/ini2py.git
cd ini2py
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
ini2py/
├── ini2py/
│   ├── __init__.py
│   ├── cli.py           # Main CLI logic
│   └── templates/       # Code generation templates
│       ├── schema.py.tpl
│       └── manager.py.tpl
├── tests/
├── examples/
├── README.md
└── pyproject.toml
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0
- Initial release
- Basic INI to Python class generation
- Type inference support
- Hot reloading with watchdog
- Sensitive data masking
- Smart path detection

## Author

**JonesHong** - [GitHub](https://github.com/joneshong)

## Support

If you encounter any issues or have questions:
- [Open an issue](https://github.com/joneshong/ini2py/issues)
- Check the [examples](examples/) directory
- Review the generated code documentation