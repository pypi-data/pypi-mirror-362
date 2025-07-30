"""
Authentication Service for Bivouac Framework.

This module provides authentication functionality using Flask-User.
"""

from typing import Optional
from flask import current_app, g
from flask_user import UserManager, current_user


class AuthService:
    """
    Authentication service for Bivouac Framework.
    
    This class provides authentication and user management functionality
    using Flask-User as the underlying authentication system.
    """
    
    _user_manager: Optional[UserManager] = None
    
    @classmethod
    def initialize(cls, app, user_model, user_manager_config=None):
        """
        Initialize the authentication service.
        
        Args:
            app: Flask application instance
            user_model: User model class
            user_manager_config: Configuration for UserManager
        """
        if user_manager_config is None:
            user_manager_config = {}
        
        cls._user_manager = UserManager(app, user_model, **user_manager_config)
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """
        Check if the current user is authenticated.
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return current_user.is_authenticated
    
    @classmethod
    def get_current_user(cls):
        """
        Get the currently authenticated user.
        
        Returns:
            Current user object or None if not authenticated
        """
        if cls.is_authenticated():
            return current_user
        return None
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """
        Get a user by their ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None if not found
        """
        if cls._user_manager is None:
            return None
        
        return cls._user_manager.db_manager.get_user_by_id(user_id)
    
    @classmethod
    def get_user_by_email(cls, email):
        """
        Get a user by their email address.
        
        Args:
            email: User email address
            
        Returns:
            User object or None if not found
        """
        if cls._user_manager is None:
            return None
        
        return cls._user_manager.db_manager.get_user_by_email(email)
    
    @classmethod
    def create_user(cls, email, password, **kwargs):
        """
        Create a new user.
        
        Args:
            email: User email address
            password: User password
            **kwargs: Additional user attributes
            
        Returns:
            Created user object
        """
        if cls._user_manager is None:
            raise RuntimeError("AuthService not initialized")
        
        user = cls._user_manager.db_manager.create_user(
            email=email,
            password=password,
            **kwargs
        )
        
        return user
    
    @classmethod
    def delete_user(cls, user):
        """
        Delete a user.
        
        Args:
            user: User object to delete
        """
        if cls._user_manager is None:
            raise RuntimeError("AuthService not initialized")
        
        cls._user_manager.db_manager.delete_user(user)
    
    @classmethod
    def change_password(cls, user, new_password):
        """
        Change a user's password.
        
        Args:
            user: User object
            new_password: New password
        """
        if cls._user_manager is None:
            raise RuntimeError("AuthService not initialized")
        
        cls._user_manager.db_manager.change_password(user, new_password)
    
    @classmethod
    def verify_password(cls, user, password):
        """
        Verify a user's password.
        
        Args:
            user: User object
            password: Password to verify
            
        Returns:
            True if password is correct, False otherwise
        """
        if cls._user_manager is None:
            return False
        
        return cls._user_manager.db_manager.verify_password(user, password)
    
    @classmethod
    def get_user_manager(cls) -> Optional[UserManager]:
        """
        Get the underlying UserManager instance.
        
        Returns:
            UserManager instance or None if not initialized
        """
        return cls._user_manager 