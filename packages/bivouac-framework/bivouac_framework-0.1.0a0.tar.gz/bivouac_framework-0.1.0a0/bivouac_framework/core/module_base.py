"""
Base Module Class for Bivouac Framework.

This module defines the abstract base class that all modules
must inherit from.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class ModuleBase(ABC):
    """
    Abstract base class for all modules in the Bivouac Framework.
    
    All modules must inherit from this class and implement
    the required methods.
    """
    
    name: str = None
    version: str = None
    description: str = None
    
    # Dependency information
    dependencies: List[str] = []
    optional_dependencies: List[str] = []
    
    def __init__(self):
        """
        Initialize the module.
        
        Subclasses should call super().__init__() and then
        perform their own initialization.
        """
        if not self.name:
            raise ValueError("Module must have a name")
        
        if not self.version:
            raise ValueError("Module must have a version")
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the module.
        
        This method is called when the module is activated.
        Subclasses should implement their initialization logic here.
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Clean up the module.
        
        This method is called when the module is deactivated.
        Subclasses should implement their cleanup logic here.
        """
        pass
    
    def get_info(self) -> dict:
        """
        Get module information.
        
        Returns:
            Dictionary containing module information
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'dependencies': self.dependencies,
            'optional_dependencies': self.optional_dependencies
        }
    
    def __str__(self) -> str:
        """String representation of the module."""
        return f"{self.name} v{self.version}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the module."""
        return f"<{self.__class__.__name__} name='{self.name}' version='{self.version}'>" 