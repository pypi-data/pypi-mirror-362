"""
Permission Service for Bivouac Framework.

This module provides role-based access control (RBAC) functionality.
"""

from typing import Dict, List, Optional, Set
from functools import wraps
from flask import current_app, g, request, abort


class PermissionService:
    """
    Permission service for Bivouac Framework.
    
    This class provides role-based access control (RBAC) functionality
    for managing user permissions and roles.
    """
    
    _permissions: Dict[str, Dict] = {}
    _roles: Dict[str, Set[str]] = {}
    _user_roles: Dict[int, Set[str]] = {}
    _cache: Dict[str, bool] = {}
    
    @classmethod
    def create_permission(cls, permission_id: str, description: str, 
                         resource_type: str = None) -> None:
        """
        Create a new permission.
        
        Args:
            permission_id: Unique permission identifier
            description: Human-readable description
            resource_type: Type of resource this permission applies to
        """
        cls._permissions[permission_id] = {
            'description': description,
            'resource_type': resource_type
        }
    
    @classmethod
    def create_role(cls, role_name: str, permissions: List[str] = None) -> None:
        """
        Create a new role with permissions.
        
        Args:
            role_name: Name of the role
            permissions: List of permission IDs
        """
        if permissions is None:
            permissions = []
        
        cls._roles[role_name] = set(permissions)
    
    @classmethod
    def assign_role_to_user(cls, user_id: int, role_name: str) -> None:
        """
        Assign a role to a user.
        
        Args:
            user_id: User ID
            role_name: Name of the role to assign
        """
        if user_id not in cls._user_roles:
            cls._user_roles[user_id] = set()
        
        cls._user_roles[user_id].add(role_name)
        cls._clear_user_cache(user_id)
    
    @classmethod
    def remove_role_from_user(cls, user_id: int, role_name: str) -> None:
        """
        Remove a role from a user.
        
        Args:
            user_id: User ID
            role_name: Name of the role to remove
        """
        if user_id in cls._user_roles:
            cls._user_roles[user_id].discard(role_name)
            cls._clear_user_cache(user_id)
    
    @classmethod
    def has_permission(cls, permission_id: str, user_id: int = None) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            permission_id: Permission ID to check
            user_id: User ID (if None, uses current user)
            
        Returns:
            True if user has permission, False otherwise
        """
        if user_id is None:
            # Get current user from Flask context
            from .auth.auth_service import AuthService
            current_user = AuthService.get_current_user()
            if current_user is None:
                return False
            user_id = current_user.id
        
        # Check cache first
        cache_key = f"{user_id}:{permission_id}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        # Check if user has any role with this permission
        user_roles = cls._user_roles.get(user_id, set())
        has_permission = False
        
        for role in user_roles:
            if role in cls._roles and permission_id in cls._roles[role]:
                has_permission = True
                break
        
        # Cache the result
        cls._cache[cache_key] = has_permission
        return has_permission
    
    @classmethod
    def get_user_permissions(cls, user_id: int) -> Set[str]:
        """
        Get all permissions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Set of permission IDs
        """
        user_roles = cls._user_roles.get(user_id, set())
        permissions = set()
        
        for role in user_roles:
            if role in cls._roles:
                permissions.update(cls._roles[role])
        
        return permissions
    
    @classmethod
    def get_user_roles(cls, user_id: int) -> Set[str]:
        """
        Get all roles for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Set of role names
        """
        return cls._user_roles.get(user_id, set()).copy()
    
    @classmethod
    def _clear_user_cache(cls, user_id: int) -> None:
        """
        Clear cache for a specific user.
        
        Args:
            user_id: User ID
        """
        keys_to_remove = [key for key in cls._cache.keys() 
                         if key.startswith(f"{user_id}:")]
        for key in keys_to_remove:
            del cls._cache[key]
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear all permission cache."""
        cls._cache.clear()
    
    @classmethod
    def get_all_permissions(cls) -> Dict[str, Dict]:
        """
        Get all registered permissions.
        
        Returns:
            Dictionary of all permissions
        """
        return cls._permissions.copy()
    
    @classmethod
    def get_all_roles(cls) -> Dict[str, Set[str]]:
        """
        Get all registered roles.
        
        Returns:
            Dictionary of all roles and their permissions
        """
        return {role: permissions.copy() for role, permissions in cls._roles.items()}


def permission_required(permission_id: str, resource_type: str = None, 
                       resource_id_arg: str = None):
    """
    Decorator to require a specific permission for a route.
    
    Args:
        permission_id: Permission ID required
        resource_type: Type of resource (for resource-specific permissions)
        resource_id_arg: Name of the argument containing resource ID
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not PermissionService.has_permission(permission_id):
                abort(403, description="Permission denied")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(role_name: str):
    """
    Decorator to require a specific role for a route.
    
    Args:
        role_name: Name of the role required
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from .auth.auth_service import AuthService
            current_user = AuthService.get_current_user()
            
            if current_user is None:
                abort(401, description="Authentication required")
            
            user_roles = PermissionService.get_user_roles(current_user.id)
            if role_name not in user_roles:
                abort(403, description="Role required")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator 