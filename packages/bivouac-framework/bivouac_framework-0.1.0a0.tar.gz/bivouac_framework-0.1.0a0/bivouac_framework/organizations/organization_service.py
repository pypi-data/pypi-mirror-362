"""
Organization Service for Bivouac Framework.

This module provides multi-tenant organization management functionality.
"""

from typing import Dict, List, Optional, Set
from datetime import datetime


class Organization:
    """
    Organization model for multi-tenant support.
    
    This class represents an organization in the system.
    """
    
    def __init__(self, id: int, name: str, description: str = None, 
                 created_at: datetime = None, updated_at: datetime = None):
        """
        Initialize an organization.
        
        Args:
            id: Organization ID
            name: Organization name
            description: Organization description
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __str__(self) -> str:
        """String representation of the organization."""
        return f"Organization(id={self.id}, name='{self.name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the organization."""
        return f"<Organization id={self.id} name='{self.name}'>"


class OrganizationService:
    """
    Organization service for Bivouac Framework.
    
    This class provides multi-tenant organization management functionality
    for isolating data between different organizations.
    """
    
    _organizations: Dict[int, Organization] = {}
    _user_organizations: Dict[int, List[int]] = {}
    _next_id = 1
    
    @classmethod
    def create_organization(cls, name: str, description: str = None) -> Organization:
        """
        Create a new organization.
        
        Args:
            name: Organization name
            description: Organization description
            
        Returns:
            Created organization
        """
        org_id = cls._next_id
        cls._next_id += 1
        
        organization = Organization(
            id=org_id,
            name=name,
            description=description
        )
        
        cls._organizations[org_id] = organization
        return organization
    
    @classmethod
    def get_organization(cls, org_id: int) -> Optional[Organization]:
        """
        Get an organization by ID.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Organization object or None if not found
        """
        return cls._organizations.get(org_id)
    
    @classmethod
    def get_all_organizations(cls) -> List[Organization]:
        """
        Get all organizations.
        
        Returns:
            List of all organizations
        """
        return list(cls._organizations.values())
    
    @classmethod
    def update_organization(cls, org_id: int, name: str = None, 
                           description: str = None) -> Optional[Organization]:
        """
        Update an organization.
        
        Args:
            org_id: Organization ID
            name: New organization name
            description: New organization description
            
        Returns:
            Updated organization or None if not found
        """
        organization = cls.get_organization(org_id)
        if organization is None:
            return None
        
        if name is not None:
            organization.name = name
        if description is not None:
            organization.description = description
        
        organization.updated_at = datetime.now()
        return organization
    
    @classmethod
    def delete_organization(cls, org_id: int) -> bool:
        """
        Delete an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            True if deleted, False if not found
        """
        if org_id not in cls._organizations:
            return False
        
        # Remove organization from all users
        for user_id in list(cls._user_organizations.keys()):
            cls._user_organizations[user_id] = [
                oid for oid in cls._user_organizations[user_id] 
                if oid != org_id
            ]
        
        del cls._organizations[org_id]
        return True
    
    @classmethod
    def add_user_to_organization(cls, user_id: int, org_id: int) -> bool:
        """
        Add a user to an organization.
        
        Args:
            user_id: User ID
            org_id: Organization ID
            
        Returns:
            True if successful, False if organization not found
        """
        if org_id not in cls._organizations:
            return False
        
        if user_id not in cls._user_organizations:
            cls._user_organizations[user_id] = []
        
        if org_id not in cls._user_organizations[user_id]:
            cls._user_organizations[user_id].append(org_id)
        
        return True
    
    @classmethod
    def remove_user_from_organization(cls, user_id: int, org_id: int) -> bool:
        """
        Remove a user from an organization.
        
        Args:
            user_id: User ID
            org_id: Organization ID
            
        Returns:
            True if successful, False if not found
        """
        if user_id in cls._user_organizations:
            try:
                cls._user_organizations[user_id].remove(org_id)
                return True
            except ValueError:
                pass
        
        return False
    
    @classmethod
    def get_user_organizations(cls, user_id: int) -> List[Organization]:
        """
        Get all organizations for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of organizations the user belongs to
        """
        org_ids = cls._user_organizations.get(user_id, [])
        return [cls._organizations[oid] for oid in org_ids 
                if oid in cls._organizations]
    
    @classmethod
    def get_user_organization(cls, user_id: int) -> Optional[Organization]:
        """
        Get the primary organization for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Primary organization or None if user has no organizations
        """
        org_ids = cls._user_organizations.get(user_id, [])
        if org_ids:
            return cls._organizations.get(org_ids[0])
        return None
    
    @classmethod
    def is_user_in_organization(cls, user_id: int, org_id: int) -> bool:
        """
        Check if a user belongs to an organization.
        
        Args:
            user_id: User ID
            org_id: Organization ID
            
        Returns:
            True if user is in organization, False otherwise
        """
        org_ids = cls._user_organizations.get(user_id, [])
        return org_id in org_ids
    
    @classmethod
    def get_organization_users(cls, org_id: int) -> List[int]:
        """
        Get all users in an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of user IDs in the organization
        """
        users = []
        for user_id, org_ids in cls._user_organizations.items():
            if org_id in org_ids:
                users.append(user_id)
        return users
    
    @classmethod
    def search_organizations(cls, query: str) -> List[Organization]:
        """
        Search organizations by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching organizations
        """
        query_lower = query.lower()
        matches = []
        
        for organization in cls._organizations.values():
            if (query_lower in organization.name.lower() or
                (organization.description and 
                 query_lower in organization.description.lower())):
                matches.append(organization)
        
        return matches 