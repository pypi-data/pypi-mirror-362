# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for YAML configuration files
- Environment variable interpolation
- Configuration schema validation
- Plugin system for custom type converters
- Configuration diff and migration tools

## [0.1.0] - 2025-01-XX

### Added
- Initial release of ini2py
- CLI tool for generating Python config classes from INI files
- Automatic type inference for int, float, bool, and string values
- Type-hinted schema classes generation
- Configuration manager with singleton pattern
- Hot reloading with watchdog file monitoring
- Sensitive data masking for security
- Smart path detection for config files
- Support for nested configuration sections
- Comprehensive test suite
- Documentation and examples
- MIT license

### Features
- **Type Safety**: Automatic type inference and conversion
- **Hot Reloading**: Real-time configuration updates
- **Security**: Automatic masking of sensitive data (passwords, API keys, secrets)
- **Developer Experience**: Full IDE autocomplete and type hints
- **Flexibility**: Support for complex configuration structures
- **Reliability**: Singleton pattern ensures consistent configuration state

### CLI Options
- `--config, -c`: Specify input INI file path
- `--output, -o`: Specify output directory for generated files
- Interactive mode with smart defaults

### Generated Files
- `schema.py`: Type-hinted configuration schema classes
- `manager.py`: Configuration manager with hot reloading

### Dependencies
- click >= 8.0 (CLI framework)
- watchdog >= 2.1.6 (File system monitoring)

### Python Support
- Python 3.8+
- Cross-platform (Windows, macOS, Linux)

### Examples
- Basic usage example with common configuration patterns
- Advanced usage example with complex multi-service configurations
- Comprehensive documentation and usage patterns

### Testing
- Unit tests for all core functionality
- CLI testing with click.testing
- Configuration validation tests
- Type inference tests
- Hot reloading tests
- Edge case handling tests