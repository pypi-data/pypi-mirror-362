# Bivouac Framework

A modular Flask framework for building scalable web applications with built-in authentication, permissions, and multi-tenant support.

## Features

- **Modular Architecture**: Dynamic module loading and management
- **Authentication System**: Flask-User based authentication with session management
- **Role-Based Access Control**: Comprehensive permission system with caching
- **Multi-Tenant Support**: Organization-based data isolation
- **CLI Tools**: Command-line interface for application management
- **Extensible**: Easy to extend with custom modules and functionality

## Quick Start

### Installation

```bash
pip install bivouac-framework
```

### Basic Usage

```python
from bivouac_framework import create_app
from bivouac_framework.core.config import Config

# Create configuration
config = Config()
config.SECRET_KEY = 'your-secret-key'
config.SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# Create application
app = create_app(config)

if __name__ == '__main__':
    app.run(debug=True)
```

### CLI Commands

```bash
# Create a new application
bivouac create-app myapp

# List available modules
bivouac list-modules

# Check version
bivouac --version
```

## Core Components

### Module System

The framework provides a dynamic module loading system:

```python
from bivouac_framework.core.module_registry import ModuleRegistry
from bivouac_framework.core.module_base import ModuleBase

class MyModule(ModuleBase):
    name = "My Module"
    version = "1.0.0"
    
    def initialize(self):
        # Module initialization code
        pass
    
    def cleanup(self):
        # Module cleanup code
        pass

# Register module
ModuleRegistry.register_module(MyModule())
```

### Authentication

Built-in authentication with Flask-User:

```python
from bivouac_framework.auth.auth_service import AuthService

# Check if user is authenticated
if AuthService.is_authenticated():
    user = AuthService.get_current_user()
    print(f"Welcome, {user.username}!")
```

### Permissions

Role-based access control system:

```python
from bivouac_framework.permissions.permission_service import PermissionService

# Create permission
PermissionService.create_permission('user.edit', 'Edit users', 'user')

# Check permission
if PermissionService.has_permission('user.edit'):
    # User can edit
    pass
```

### Organizations

Multi-tenant organization support:

```python
from bivouac_framework.organizations.organization_service import OrganizationService

# Get user's organization
org = OrganizationService.get_user_organization(user_id)

# Create organization
new_org = OrganizationService.create_organization('My Company')
```

## Module Development

### Creating a Module

1. **Structure your module**:
```
my_module/
├── __init__.py
├── routes.py
├── models.py
├── services/
├── templates/
└── static/
```

2. **Define your module class**:
```python
# my_module/__init__.py
from bivouac_framework.core.module_base import ModuleBase
from flask import Blueprint

class MyModule(ModuleBase):
    name = "My Module"
    version = "1.0.0"
    
    def __init__(self):
        self.blueprint = Blueprint('my_module', __name__)
        self.register_routes()
    
    def register_routes(self):
        from . import routes
        # Register routes here
```

3. **Register your module**:
```python
from bivouac_framework.core.module_registry import ModuleRegistry
from my_module import MyModule

ModuleRegistry.register_module(MyModule())
```

### Module Lifecycle

Modules follow a specific lifecycle:

1. **Registration**: Module is registered with the system
2. **Initialization**: `initialize()` method is called
3. **Activation**: Module becomes active and available
4. **Runtime**: Module is used during application execution
5. **Cleanup**: `cleanup()` method is called on shutdown

## Configuration

The framework uses a configuration system that supports multiple environments:

```python
from bivouac_framework.core.config import Config

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/prod'
```

## API Reference

### Core Classes

- `ModuleRegistry`: Manages module registration and lifecycle
- `ModuleBase`: Base class for all modules
- `Config`: Configuration management
- `AuthService`: Authentication and user management
- `PermissionService`: Permission and role management
- `OrganizationService`: Multi-tenant organization management

### CLI Commands

- `bivouac create-app <name>`: Create a new application
- `bivouac list-modules`: List available modules
- `bivouac --version`: Show version information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Join our community discussions

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history. 