"""
Core components of the Bivouac Framework.

This package contains the fundamental building blocks of the framework:
- Module registry for dynamic module management
- Base module class for all modules
- Configuration management
"""

from .module_registry import ModuleRegistry
from .module_base import ModuleBase
from .config import Config

__all__ = ['ModuleRegistry', 'ModuleBase', 'Config'] 