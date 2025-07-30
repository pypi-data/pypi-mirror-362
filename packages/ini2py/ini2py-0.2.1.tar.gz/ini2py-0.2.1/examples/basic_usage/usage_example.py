#!/usr/bin/env python3
"""
Basic usage example for ini2py.

This script demonstrates how to use the generated configuration classes
after running `ini2py` on the config.ini file.

To run this example:
1. Navigate to this directory
2. Run: ini2py --config config.ini --output ./generated
3. Run: python usage_example.py
"""

import sys
import time
import os

# Add the generated config to Python path
sys.path.insert(0, './generated')

try:
    from generated.manager import ConfigManager
    print("✅ Successfully imported ConfigManager")
except ImportError as e:
    print(f"❌ Failed to import ConfigManager: {e}")
    print("\n🔧 To fix this, run:")
    print("   ini2py --config config.ini --output ./generated")
    sys.exit(1)


def main():
    """Demonstrate basic configuration usage."""
    print("🚀 ini2py Basic Usage Example")
    print("=" * 40)
    
    # Initialize configuration manager (singleton pattern)
    config = ConfigManager()
    print("✅ ConfigManager initialized")
    
    # Access configuration with full type hints and autocomplete
    print("\n📋 System Configuration:")
    print(f"  Mode: {config.system.mode}")
    print(f"  Debug: {config.system.debug}")
    print(f"  Port: {config.system.port}")
    print(f"  Timeout: {config.system.timeout}s")
    print(f"  App Name: {config.system.name}")
    print(f"  Version: {config.system.version}")
    
    print("\n🗄️  Database Configuration:")
    print(f"  Host: {config.database.host}")
    print(f"  Port: {config.database.port}")
    print(f"  Database: {config.database.name}")
    print(f"  User: {config.database.user}")
    print(f"  Pool Size: {config.database.pool_size}")
    print(f"  SSL Mode: {config.database.ssl_mode}")
    # Note: password will be masked in logs
    
    print("\n🔴 Redis Configuration:")
    print(f"  Host: {config.redis.host}")
    print(f"  Port: {config.redis.port}")
    print(f"  Database: {config.redis.db}")
    print(f"  Max Connections: {config.redis.max_connections}")
    
    print("\n📝 Logging Configuration:")
    print(f"  Level: {config.logging.level}")
    print(f"  File Path: {config.logging.file_path}")
    print(f"  Max File Size: {config.logging.max_file_size}MB")
    print(f"  Backup Count: {config.logging.backup_count}")
    
    print("\n🌐 API Configuration:")
    print(f"  Base URL: {config.api.base_url}")
    print(f"  Version: {config.api.version}")
    print(f"  Rate Limit: {config.api.rate_limit}")
    print(f"  Enable Retries: {config.api.enable_retries}")
    print(f"  Max Retries: {config.api.max_retries}")
    
    # Demonstrate sensitive data masking
    print("\n🔒 Sensitive Data Handling:")
    print("Database properties (masked):")
    db_props = config.database.return_properties(return_type='list', mask_sensitive=True)
    for prop in db_props:
        if 'password' in prop.lower():
            print(f"  {prop}")
    
    print("\nAPI properties (masked):")
    api_props = config.api.return_properties(return_type='list', mask_sensitive=True)
    for prop in api_props:
        if 'key' in prop.lower():
            print(f"  {prop}")
    
    # Demonstrate type inference
    print("\n🔢 Type Inference Examples:")
    print(f"  config.system.port type: {type(config.system.port).__name__}")
    print(f"  config.system.debug type: {type(config.system.debug).__name__}")
    print(f"  config.system.timeout type: {type(config.system.timeout).__name__}")
    print(f"  config.system.mode type: {type(config.system.mode).__name__}")
    
    # Demonstrate configuration as dictionary
    print("\n📊 Configuration as Dictionary:")
    system_dict = config.system.return_properties(return_type='dict', mask_sensitive=False)
    print("System configuration:")
    for key, value in system_dict.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Demonstrate hot reloading
    print("\n🔄 Hot Reloading Demo")
    print("The configuration manager is now watching for file changes.")
    print("Try editing config.ini and save it to see automatic reloading!")
    print("Press Ctrl+C to exit.")
    
    try:
        # Monitor configuration changes
        last_port = config.system.port
        print(f"\nInitial port: {last_port}")
        
        while True:
            time.sleep(2)
            current_port = config.system.port
            if current_port != last_port:
                print(f"🔄 Port changed from {last_port} to {current_port}!")
                last_port = current_port
            else:
                print(".", end="", flush=True)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")


if __name__ == "__main__":
    main()