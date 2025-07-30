# AD User Manager

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Modern Active Directory user management tool with conflict resolution, supporting both domain controller (PowerShell) and remote LDAP operations.

## Features

- **Dual Operation Modes**: PowerShell on domain controllers for optimal performance, LDAP for remote connections
- **Automatic Conflict Resolution**: Intelligent username conflict detection and resolution
- **Type-Safe Configuration**: Pydantic-based configuration with validation
- **Rich CLI Interface**: Beautiful command-line interface with progress indicators
- **Structured Logging**: JSON and console logging with contextual information
- **Modern Python**: Built for Python 3.12+ with type hints and async support

## Installation

```bash
pip install ad-user-manager
```

## Quick Start

### Domain Controller Mode (Recommended)

When running directly on a domain controller, the tool automatically uses PowerShell for optimal performance:

```python
from ad_user_manager import ADConfig, DCServerConfig, create_ad_manager

# Configure for domain controller
config = ADConfig(
    server=DCServerConfig(
        connection_type="domain_controller",
        base_dn="CN=Users,DC=example,DC=com",
        use_current_credentials=True  # Use current user's AD credentials
    )
)

# Create user
with create_ad_manager(config) as manager:
    result = manager.create_user(
        username="jdoe",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        resolve_conflicts=True
    )
    print(f"Created user: {result.username}")
```

### LDAP Mode (Remote Connections)

For remote connections to Active Directory:

```python
from ad_user_manager import ADConfig, LDAPServerConfig, create_ad_manager

# Configure for LDAP connection
config = ADConfig(
    server=LDAPServerConfig(
        connection_type="ldap",
        host="dc.example.com",
        port=389,
        use_ssl=False,
        bind_dn="CN=service-account,CN=Users,DC=example,DC=com",
        bind_password="your-password",
        base_dn="CN=Users,DC=example,DC=com"
    )
)

# Create user
with create_ad_manager(config) as manager:
    result = manager.create_user(
        username="jsmith",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com"
    )
```

## CLI Usage

### Create a User

```bash
# Domain controller mode
ad-user-manager create-user -u jdoe -f John -l Doe -e john.doe@example.com

# With conflict resolution
ad-user-manager create-user -u jdoe -f John -l Doe -e john.doe@example.com --resolve-conflicts

# Dry run mode
ad-user-manager create-user -u jdoe -f John -l Doe -e john.doe@example.com --dry-run
```

### Search for a User

```bash
ad-user-manager search-user -u jdoe
```

### Test Connection

```bash
ad-user-manager test-connection
```

### Generate Username Suggestions

```bash
ad-user-manager suggest-usernames -f John -l Doe
```

## Configuration

### Environment Variables

```bash
# LDAP Configuration
export AD_CONNECTION_TYPE=ldap
export AD_HOST=dc.example.com
export AD_PORT=389
export AD_USE_SSL=false
export AD_BIND_DN="CN=service-account,CN=Users,DC=example,DC=com"
export AD_BIND_PASSWORD="your-password"
export AD_BASE_DN="CN=Users,DC=example,DC=com"

# Domain Controller Configuration
export AD_CONNECTION_TYPE=domain_controller
export AD_BASE_DN="CN=Users,DC=example,DC=com"
export AD_USE_CURRENT_CREDENTIALS=true
```

### Configuration File

Create a `.env` file or use environment variables:

```ini
# For LDAP mode
AD_CONNECTION_TYPE=ldap
AD_HOST=dc.example.com
AD_BIND_DN=CN=service-account,CN=Users,DC=example,DC=com
AD_BIND_PASSWORD=your-password
AD_BASE_DN=CN=Users,DC=example,DC=com

# For DC mode
AD_CONNECTION_TYPE=domain_controller
AD_BASE_DN=CN=Users,DC=example,DC=com
AD_USE_CURRENT_CREDENTIALS=true
```

## Advanced Features

### Conflict Resolution

The tool automatically detects username conflicts and generates alternatives:

```python
# Automatic conflict resolution
result = manager.create_user(
    username="jdoe",  # If exists, might become "jdoe1", "jdoe2", etc.
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    resolve_conflicts=True
)
print(f"Final username: {result.username}")
print(f"Conflicts resolved: {result.conflicts_resolved}")
```

### Custom Attributes

```python
result = manager.create_user(
    username="jdoe",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    additional_attributes={
        "department": "Engineering",
        "title": "Software Developer",
        "telephoneNumber": "+1-555-0123"
    }
)
```

### Logging Configuration

```python
config = ADConfig(
    server=your_server_config,
    log_level="DEBUG",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_format="json"   # "json" or "console"
)
```

## Development

### Setup

```bash
git clone https://github.com/your-org/ad-user-manager.git
cd ad-user-manager
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
black .

# Type checking
mypy .
```

## Architecture

The project is organized into focused modules:

- `models.py` - Data models and configuration schemas
- `powershell_manager.py` - PowerShell-based AD operations (DC mode)
- `ldap_manager.py` - LDAP-based AD operations (remote mode)
- `factory.py` - Manager creation and auto-detection
- `config.py` - Configuration management
- `validators.py` - Input validation and conflict resolution
- `exceptions.py` - Custom exception hierarchy
- `cli.py` - Command-line interface
- `utils.py` - Utility functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, feature requests, or questions:

1. Check the [GitHub Issues](https://github.com/your-org/ad-user-manager/issues)
2. Create a new issue with detailed information
3. Include configuration (without sensitive data) and error messages
