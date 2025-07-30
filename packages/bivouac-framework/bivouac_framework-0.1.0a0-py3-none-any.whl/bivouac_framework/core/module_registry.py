"""
Module Registry for Bivouac Framework.

This module provides a centralized registry for managing modules,
their dependencies, and lifecycle.
"""

from typing import Dict, List, Optional, Set
from .module_base import ModuleBase


class ModuleRegistry:
    """
    Central registry for managing modules in the Bivouac Framework.
    
    This class handles module registration, dependency resolution,
    and lifecycle management.
    """
    
    _modules: Dict[str, ModuleBase] = {}
    _active_modules: Set[str] = set()
    _app = None
    
    @classmethod
    def register_module(cls, module: ModuleBase, dependencies: List[str] = None, 
                       optional_dependencies: List[str] = None) -> None:
        """
        Register a module with the registry.
        
        Args:
            module: The module instance to register
            dependencies: List of required module dependencies
            optional_dependencies: List of optional module dependencies
        """
        if not isinstance(module, ModuleBase):
            raise ValueError("Module must inherit from ModuleBase")
        
        module_name = module.name
        if module_name in cls._modules:
            raise ValueError(f"Module '{module_name}' is already registered")
        
        # Store module with dependency information
        module.dependencies = dependencies or []
        module.optional_dependencies = optional_dependencies or []
        cls._modules[module_name] = module
        
        print(f"Registered module: {module_name}")
    
    @classmethod
    def get_module(cls, name: str) -> Optional[ModuleBase]:
        """
        Get a registered module by name.
        
        Args:
            name: The name of the module
            
        Returns:
            The module instance or None if not found
        """
        return cls._modules.get(name)
    
    @classmethod
    def get_all_modules(cls) -> List[ModuleBase]:
        """
        Get all registered modules.
        
        Returns:
            List of all registered modules
        """
        return list(cls._modules.values())
    
    @classmethod
    def get_active_modules(cls) -> List[ModuleBase]:
        """
        Get all active modules.
        
        Returns:
            List of active modules
        """
        return [cls._modules[name] for name in cls._active_modules 
                if name in cls._modules]
    
    @classmethod
    def is_active(cls, module_name: str) -> bool:
        """
        Check if a module is active.
        
        Args:
            module_name: The name of the module
            
        Returns:
            True if the module is active, False otherwise
        """
        return module_name in cls._active_modules
    
    @classmethod
    def initialize(cls, app) -> None:
        """
        Initialize the module registry with a Flask app.
        
        Args:
            app: Flask application instance
        """
        cls._app = app
        
        # Resolve dependencies and activate modules
        cls._resolve_dependencies()
        
        # Initialize active modules
        for module in cls.get_active_modules():
            try:
                module.initialize()
                print(f"Activated module: {module.name}")
            except Exception as e:
                print(f"Failed to initialize module {module.name}: {e}")
    
    @classmethod
    def _resolve_dependencies(cls) -> None:
        """
        Resolve module dependencies and determine activation order.
        """
        # Simple dependency resolution - in a real implementation,
        # this would be more sophisticated with cycle detection
        resolved = set()
        
        for module_name, module in cls._modules.items():
            if cls._can_activate(module, resolved):
                cls._active_modules.add(module_name)
                resolved.add(module_name)
    
    @classmethod
    def _can_activate(cls, module: ModuleBase, resolved: Set[str]) -> bool:
        """
        Check if a module can be activated based on its dependencies.
        
        Args:
            module: The module to check
            resolved: Set of already resolved module names
            
        Returns:
            True if the module can be activated
        """
        # Check required dependencies
        for dep in module.dependencies:
            if dep not in cls._modules:
                print(f"Warning: Required dependency '{dep}' for module '{module.name}' not found")
                return False
            if dep not in resolved:
                return False
        
        return True
    
    @classmethod
    def cleanup(cls) -> None:
        """
        Clean up all active modules.
        """
        for module in cls.get_active_modules():
            try:
                module.cleanup()
                print(f"Cleaned up module: {module.name}")
            except Exception as e:
                print(f"Failed to cleanup module {module.name}: {e}")
        
        cls._active_modules.clear()
        cls._modules.clear()
        cls._app = None 