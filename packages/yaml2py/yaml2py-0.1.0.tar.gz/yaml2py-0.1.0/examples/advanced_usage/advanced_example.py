#!/usr/bin/env python3
"""
Advanced usage example for yaml2py

This example demonstrates:
- Complex nested structures
- Lists of objects
- Multi-level configuration hierarchies
- Dynamic configuration access
- Production-ready patterns

To run this example:
1. Navigate to this directory
2. Run: yaml2py --config config.yaml --output ./generated
3. Run: python advanced_example.py
"""

import sys

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


def display_api_endpoints():
    """Display API endpoint configuration."""
    config = ConfigManager()
    print("\n📡 API Endpoints:")
    print(f"Base URL: {config.services.api.base_url}")
    print(f"Version: {config.services.api.version}")
    print("\nEndpoints:")
    
    for endpoint in config.services.api.endpoints:
        auth_status = "🔒" if endpoint.auth_required else "🔓"
        print(f"  {auth_status} {endpoint.method:6} {endpoint.path}")
        print(f"      Rate limit: {endpoint.rate_limit} req/min")


def display_database_config():
    """Display database configuration."""
    config = ConfigManager()
    print("\n🗄️  Database Configuration:")
    
    # Primary database
    primary = config.services.database.primary
    print(f"\nPrimary Database:")
    print(f"  Engine: {primary.engine}")
    print(f"  Host: {primary.host}:{primary.port}")
    print(f"  Database: {primary.name}")
    print(f"  User: {primary.user}")
    print(f"  Password: {primary.password}")  # Masked automatically
    print(f"  Pool Size: {primary.options.pool_size}")
    print(f"  Max Overflow: {primary.options.max_overflow}")
    
    # Replica database
    replica = config.services.database.replica
    print(f"\nReplica Database:")
    print(f"  Engine: {replica.engine}")
    print(f"  Host: {replica.host}:{replica.port}")
    print(f"  Database: {replica.name}")
    print(f"  User: {replica.user}")
    print(f"  Password: {replica.password}")  # Masked automatically
    print(f"  Pool Size: {replica.options.pool_size}")


def display_monitoring_config():
    """Display monitoring configuration."""
    config = ConfigManager()
    print("\n📊 Monitoring Configuration:")
    
    # Metrics
    metrics = config.monitoring.metrics
    print(f"\nMetrics:")
    print(f"  Enabled: {metrics.enabled}")
    print(f"  Interval: {metrics.interval}s")
    print(f"  Exporters:")
    
    for exporter in metrics.exporters:
        print(f"    - {exporter.type}")
        if exporter.type == "prometheus":
            print(f"      Port: {exporter._data.get('port', 'N/A')}")
        elif exporter.type == "datadog":
            print(f"      API Key: {exporter._data.get('api_key', 'N/A')}")
            print(f"      App Key: {exporter._data.get('app_key', 'N/A')}")
    
    # Logging
    logging = config.monitoring.logging
    print(f"\nLogging:")
    print(f"  Level: {logging.level}")
    print(f"  Handlers:")
    
    for handler in logging.handlers:
        print(f"    - {handler.type}")
        if handler.type == "file":
            print(f"      Path: {handler._data.get('path', 'N/A')}")
            print(f"      Max Bytes: {handler._data.get('max_bytes', 'N/A')}")
            print(f"      Backup Count: {handler._data.get('backup_count', 'N/A')}")
        elif handler.type == "syslog":
            print(f"      Host: {handler._data.get('host', 'N/A')}:{handler._data.get('port', 'N/A')}")
            print(f"      Facility: {handler._data.get('facility', 'N/A')}")


def display_deployment_config():
    """Display deployment configuration."""
    config = ConfigManager()
    print("\n🌍 Deployment Regions:")
    
    for region in config.deployment.regions:
        primary_flag = "⭐" if region.primary else "  "
        print(f"  {primary_flag} {region.name}")
        print(f"      Replicas: {region.replicas}")


def display_features_config():
    """Display features configuration."""
    config = ConfigManager()
    print("\n🔧 Application Features:")
    
    # Authentication
    auth = config.app.features.authentication
    print(f"\nAuthentication:")
    print(f"  Enabled: {auth.enabled}")
    if auth.enabled:
        print(f"  Providers:")
        for provider in auth.providers:
            print(f"    - {provider.name}")
            if provider.name == "oauth2":
                print(f"      Client ID: {provider.client_id}")
                print(f"      Client Secret: {provider.client_secret}")  # Masked
            elif provider.name == "jwt":
                # JWT provider has different attributes, access via _data
                print(f"      Secret Key: {provider._data.get('secret_key', 'N/A')}")
                print(f"      Expiry: {provider._data.get('expiry', 'N/A')}s")
    
    # Caching
    caching = config.app.features.caching
    print(f"\nCaching:")
    print(f"  Enabled: {caching.enabled}")
    if caching.enabled:
        print(f"  Backend: {caching.backend}")
        print(f"  TTL: {caching.ttl}s")


def main():
    """Main function demonstrating advanced yaml2py usage."""
    print("🚀 yaml2py Advanced Usage Example")
    print("=" * 50)
    
    # Initialize configuration manager
    config = ConfigManager()
    print("✅ ConfigManager initialized")
    
    # Display application info
    print(f"\n📱 Application: {config.app.name} v{config.app.version}")
    print(f"Environment: {config.app.environment}")
    
    # Display various configuration sections
    display_features_config()
    display_api_endpoints()
    display_database_config()
    display_monitoring_config()
    display_deployment_config()
    
    # Demonstrate dynamic access
    print("\n🎯 Dynamic Configuration Access:")
    
    # Count total endpoints
    total_endpoints = len(config.services.api.endpoints)
    auth_required = sum(1 for ep in config.services.api.endpoints if ep.auth_required)
    print(f"  Total API endpoints: {total_endpoints}")
    print(f"  Requiring auth: {auth_required}")
    print(f"  Public endpoints: {total_endpoints - auth_required}")
    
    # Calculate total replicas
    total_replicas = sum(region.replicas for region in config.deployment.regions)
    print(f"  Total deployment replicas: {total_replicas}")
    
    # Show type safety
    print("\n🔒 Type Safety Demonstration:")
    print(f"  metrics.interval is int: {isinstance(config.monitoring.metrics.interval, int)}")
    print(f"  auth.enabled is bool: {isinstance(config.app.features.authentication.enabled, bool)}")
    print(f"  api.endpoints is list: {isinstance(config.services.api.endpoints, list)}")
    
    print("\n✨ This example demonstrates yaml2py's ability to handle")
    print("   complex, production-ready configuration structures!")


if __name__ == "__main__":
    main()