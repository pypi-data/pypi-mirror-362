# yaml2py Examples

This directory contains practical examples demonstrating how to use yaml2py in different scenarios.

## Examples Overview

### 1. Basic Usage (`basic_usage/`)

A simple example showing fundamental yaml2py features:
- Basic configuration file structure
- Type inference (int, float, bool, string)
- Sensitive data masking
- Hot reloading
- Configuration access patterns

**Files:**
- `config.yaml` - Sample configuration file
- `usage_example.py` - Basic usage demonstration

**To run:**
```bash
cd basic_usage/
yaml2py --config config.yaml --output ./generated
python usage_example.py
```

### 2. Advanced Usage (`advanced_usage/`)

A comprehensive example showing advanced features:
- Complex multi-section configurations
- Database connection management
- External API configurations
- Security settings with sensitive data
- Feature flags and A/B testing
- Performance monitoring settings
- Backup and storage configurations
- Configuration validation
- Type safety demonstrations

**Files:**
- `config.yaml` - Complex configuration file
- `advanced_example.py` - Advanced usage patterns

**To run:**
```bash
cd advanced_usage/
yaml2py --config config.yaml --output ./generated
python advanced_example.py
```

## What Each Example Demonstrates

### Basic Usage Example

**Configuration Sections:**
- `[system]` - Application settings
- `[database]` - Database connection
- `[redis]` - Cache configuration
- `[logging]` - Logging settings
- `[api]` - External API settings

**Key Features Shown:**
- ✅ Type inference and conversion
- ✅ Sensitive data masking (passwords, API keys)
- ✅ Hot reloading with file watching
- ✅ Configuration as dictionaries vs. objects
- ✅ IDE autocomplete and type hints

### Advanced Usage Example

**Configuration Sections:**
- `[app_server]` - Application server settings
- `[security]` - Security policies and secrets
- `[database_primary]` - Primary database
- `[database_replica]` - Read replica database
- `[redis_cluster]` - Redis cluster configuration
- `[elasticsearch]` - Search engine settings
- `[message_queue]` - RabbitMQ configuration
- `[monitoring]` - Observability settings
- `[feature_flags]` - A/B testing flags
- `[external_apis]` - Third-party integrations
- `[backup_storage]` - S3 backup settings
- `[performance]` - Performance tuning

**Key Features Shown:**
- ✅ Configuration validation
- ✅ Multiple database management
- ✅ Feature flag patterns
- ✅ Security-first design
- ✅ Performance monitoring integration
- ✅ Complex nested configurations
- ✅ Type safety enforcement

## Generated File Structure

After running `yaml2py`, you'll get:

```
generated/
├── schema.py    # Type-hinted schema classes
└── manager.py   # Configuration manager with hot reloading
```

## Usage Patterns

### 1. Basic Configuration Access

```python
from generated.manager import ConfigManager

config = ConfigManager()
# Access with full type hints
port = config.system.port          # int
debug = config.system.debug        # bool
timeout = config.system.timeout    # float
```

### 2. Sensitive Data Handling

```python
# Automatic masking in logs/debug output
props = config.database.return_properties(return_type='list')
print(props)  # password will be masked as "se****23"

# Get actual values for use in code
actual_password = config.database.password  # "secret123"
```

### 3. Configuration Validation

```python
class ConfigValidator:
    @staticmethod
    def validate_database_config(db_config):
        if db_config.port < 1 or db_config.port > 65535:
            raise ValueError(f"Invalid port: {db_config.port}")
        return True
```

### 4. Feature Flags

```python
def is_feature_enabled(config, feature_name: str) -> bool:
    return getattr(config.feature_flags, f"enable_{feature_name}", False)

# Usage
if is_feature_enabled(config, 'new_ui'):
    # Enable new UI features
    pass
```

### 5. Hot Reloading

```python
# Configuration automatically reloads when files change
last_port = config.system.port
while True:
    current_port = config.system.port
    if current_port != last_port:
        print(f"Port changed: {last_port} → {current_port}")
        last_port = current_port
    time.sleep(1)
```

## Common Configuration Patterns

### Database Configurations

```ini
[database]
host = localhost
port = 5432
name = myapp
user = admin
password = secret123
pool_size = 10
timeout = 30
ssl_mode = require
```

### API Configurations

```ini
[api]
base_url = https://api.example.com
api_key = sk-1234567890abcdef
timeout = 30
retries = 3
enable_circuit_breaker = true
```

### Security Settings

```ini
[security]
secret_key = super-secret-key
jwt_expiry_hours = 24
session_timeout = 1800
enable_rate_limiting = true
rate_limit_per_minute = 100
```

## Tips for Effective Configuration Management

1. **Group Related Settings**: Use logical section names like `[database]`, `[redis]`, `[security]`

2. **Use Descriptive Names**: Prefer `connection_timeout` over `timeout` for clarity

3. **Leverage Type Inference**: Use `true`/`false` for booleans, numbers for ints/floats

4. **Secure Sensitive Data**: yaml2py automatically masks fields containing:
   - `password`, `secret`, `key`, `token`, `api_key`

5. **Document Your Config**: Use comments in YAML files to explain complex settings

6. **Validate Early**: Add validation logic to catch configuration errors at startup

7. **Use Environment-Specific Configs**: Consider separate config files for dev/staging/prod

## Troubleshooting

### Import Errors
```bash
# Make sure to generate files first
yaml2py --config config.yaml --output ./generated

# Check Python path
export PYTHONPATH="${PYTHONPATH}:./generated"
```

### Type Conversion Issues
```python
# yaml2py infers types from string values:
# "123" → int
# "12.34" → float  
# "true"/"false" → bool
# "anything else" → str
```

### Hot Reloading Not Working
- Ensure the config file path is accessible
- Check file permissions
- Verify the watchdog is properly installed

## Next Steps

- Review the generated `schema.py` to understand the type-hinted classes
- Examine `manager.py` to see the singleton pattern and file watching
- Customize the examples for your specific use case
- Add validation logic for your configuration requirements
- Integrate with your application's logging and monitoring systems