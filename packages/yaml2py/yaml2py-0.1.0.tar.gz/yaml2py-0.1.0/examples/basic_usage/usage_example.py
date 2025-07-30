#!/usr/bin/env python3
"""
Basic usage example for yaml2py

This example demonstrates:
- Loading configuration from YAML
- Accessing typed configuration values
- Singleton pattern
- Type safety
- Hot reloading

To run this example:
1. Navigate to this directory
2. Run: yaml2py --config config.yaml --output ./generated
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
    print("   yaml2py --config config.yaml --output ./generated")
    sys.exit(1)


def main():
    """Demonstrate basic configuration usage."""
    print("🚀 yaml2py Basic Usage Example")
    print("=" * 40)
    
    # Initialize configuration manager (singleton pattern)
    config = ConfigManager()
    print("✅ ConfigManager initialized")
    
    # Access configuration with full type hints and autocomplete
    print("\n📋 Application Configuration:")
    print(f"  Name: {config.app.name}")
    print(f"  Version: {config.app.version}")
    print(f"  Debug: {config.app.debug}")
    
    print("\n🌐 Server Configuration:")
    print(f"  Host: {config.server.host}")
    print(f"  Port: {config.server.port}")
    print(f"  Workers: {config.server.workers}")
    
    print("\n🗄️  Database Configuration:")
    print(f"  Engine: {config.database.engine}")
    print(f"  Host: {config.database.host}")
    print(f"  Port: {config.database.port}")
    print(f"  Database: {config.database.name}")
    print(f"  User: {config.database.user}")
    print(f"  Password: {config.database.password}  # Automatically masked!")
    
    print("\n📝 Logging Configuration:")
    print(f"  Level: {config.logging.level}")
    print(f"  Format: {config.logging.format}")
    print(f"  Output: {config.logging.output}")
    
    # Demonstrate type inference
    print("\n🔢 Type Inference Examples:")
    print(f"  config.app.debug type: {type(config.app.debug).__name__}")
    print(f"  config.server.port type: {type(config.server.port).__name__}")
    print(f"  config.app.name type: {type(config.app.name).__name__}")
    print(f"  config.server.workers type: {type(config.server.workers).__name__}")
    
    # Demonstrate configuration as dictionary
    print("\n📊 Configuration as Dictionary:")
    app_dict = config.app.return_properties(return_type='dict', mask_sensitive=False)
    print("App configuration:")
    for key, value in app_dict.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Demonstrate sensitive data masking
    print("\n🔒 Sensitive Data Handling:")
    print("Database properties (masked):")
    db_props = config.database.return_properties(return_type='list', mask_sensitive=True)
    for prop in db_props:
        if 'password' in prop.lower():
            print(f"  {prop}")
    
    # Demonstrate hot reloading
    print("\n🔄 Hot Reloading Demo")
    print("The configuration manager is now watching for file changes.")
    print("Try editing config.yaml and save it to see automatic reloading!")
    print("Press Ctrl+C to exit.")
    
    try:
        # Monitor configuration changes
        last_debug = config.app.debug
        print(f"\nInitial debug mode: {last_debug}")
        
        while True:
            time.sleep(2)
            current_debug = config.app.debug
            if current_debug != last_debug:
                print(f"🔄 Debug mode changed from {last_debug} to {current_debug}!")
                last_debug = current_debug
            else:
                print(".", end="", flush=True)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")


if __name__ == "__main__":
    main()