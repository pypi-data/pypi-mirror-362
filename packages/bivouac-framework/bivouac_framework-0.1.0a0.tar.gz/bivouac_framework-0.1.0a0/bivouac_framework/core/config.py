"""
Configuration Management for Bivouac Framework.

This module provides configuration management for the framework,
supporting multiple environments and configuration sources.
"""

import os
from typing import Any, Dict, Optional


class Config:
    """
    Configuration class for Bivouac Framework.
    
    This class provides a centralized way to manage configuration
    settings for the framework and applications.
    """
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    
    # Module configuration
    MODULE_AUTO_DISCOVERY = True
    MODULE_DISCOVERY_PATHS = ['modules', 'core_modules', 'custom_modules']
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    @classmethod
    def init_app(cls, app):
        """
        Initialize configuration with Flask app.
        
        Args:
            app: Flask application instance
        """
        # Set configuration from environment variables
        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                env_value = os.environ.get(key)
                if env_value is not None:
                    setattr(cls, key, env_value)
        
        # Apply configuration to app
        app.config.from_object(cls)
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(cls, key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        setattr(cls, key, value)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        config_dict = {}
        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                config_dict[key] = getattr(cls, key)
        return config_dict


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    LOG_LEVEL = 'WARNING'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 