"""
Test imports for Bivouac Framework.

This module tests that all core components can be imported correctly.
"""

import sys
import os

# Add the package to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_core_imports():
    """Test that core components can be imported."""
    try:
        from bivouac_framework import (
            ModuleRegistry, ModuleBase, Config, AuthService, 
            PermissionService, OrganizationService, create_app, __version__
        )
        print("✅ Core imports successful")
        print(f"   Version: {__version__}")
        return True
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False


def test_module_registry():
    """Test module registry functionality."""
    try:
        from bivouac_framework.core.module_registry import ModuleRegistry
        from bivouac_framework.core.module_base import ModuleBase
        
        # Test basic functionality
        modules = ModuleRegistry.get_all_modules()
        print(f"✅ Module registry test successful - {len(modules)} modules registered")
        return True
    except Exception as e:
        print(f"❌ Module registry test failed: {e}")
        return False


def test_config():
    """Test configuration functionality."""
    try:
        from bivouac_framework.core.config import Config, DevelopmentConfig
        
        # Test configuration
        config = Config()
        dev_config = DevelopmentConfig()
        
        print("✅ Configuration test successful")
        print(f"   Debug mode: {dev_config.DEBUG}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_services():
    """Test service imports."""
    try:
        from bivouac_framework.auth.auth_service import AuthService
        from bivouac_framework.permissions.permission_service import PermissionService
        from bivouac_framework.organizations.organization_service import OrganizationService
        
        print("✅ Service imports successful")
        return True
    except ImportError as e:
        print(f"❌ Service import failed: {e}")
        return False


def test_cli():
    """Test CLI functionality."""
    try:
        from bivouac_framework.cli.commands import main
        
        print("✅ CLI import successful")
        return True
    except ImportError as e:
        print(f"❌ CLI import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Bivouac Framework imports...")
    print("=" * 50)
    
    tests = [
        test_core_imports,
        test_module_registry,
        test_config,
        test_services,
        test_cli
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 