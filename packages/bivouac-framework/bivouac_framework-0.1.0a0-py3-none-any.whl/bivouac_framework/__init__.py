"""
Bivouac Framework - A modular Flask framework for building scalable web applications.

This package provides a comprehensive framework for building modular web applications
with built-in authentication, permissions, and multi-tenant support.
"""

__version__ = "0.1.0-alpha"
__author__ = "Bivouac Framework Team"
__email__ = "team@bivouac-framework.com"

# Core imports
from .core.module_registry import ModuleRegistry
from .core.module_base import ModuleBase
from .core.config import Config

# Service imports
from .auth.auth_service import AuthService
from .permissions.permission_service import PermissionService
from .organizations.organization_service import OrganizationService

# Application factory
def create_app(config=None):
    """
    Create and configure a Flask application with Bivouac Framework.
    
    Args:
        config: Configuration object or class
        
    Returns:
        Flask application instance
    """
    from flask import Flask
    
    app = Flask(__name__)
    
    if config:
        app.config.from_object(config)
    
    # Initialize core components
    ModuleRegistry.initialize(app)
    
    # Register blueprints and routes
    for module in ModuleRegistry.get_active_modules():
        if hasattr(module, 'blueprint'):
            app.register_blueprint(module.blueprint)
    
    return app

# Export main classes
__all__ = [
    'ModuleRegistry',
    'ModuleBase', 
    'Config',
    'AuthService',
    'PermissionService',
    'OrganizationService',
    'create_app',
    '__version__',
] 