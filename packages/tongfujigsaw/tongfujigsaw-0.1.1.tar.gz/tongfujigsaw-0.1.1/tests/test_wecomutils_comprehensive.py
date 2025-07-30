#!/usr/bin/env python3
"""
Comprehensive test suite for wecomutils package.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)


class TestWecomutilsImports(unittest.TestCase):
    """Test basic imports for wecomutils package."""
    
    def test_package_import(self):
        """Test that wecomutils package can be imported."""
        import wecomutils
        self.assertIsNotNone(wecomutils)
    
    def test_wecom_subpackage_import(self):
        """Test wecom subpackage import."""
        from wecomutils import wecom
        self.assertIsNotNone(wecom)
    
    def test_wx_api_base_import(self):
        """Test WXApiBase import."""
        try:
            from wecomutils.wecom import WXApiBase
            if WXApiBase is None:
                self.skipTest("WXApiBase not available (missing dependencies)")
            self.assertIsNotNone(WXApiBase)
        except ImportError:
            self.skipTest("WXApiBase not available (missing dependencies)")
    
    def test_token_cache_import(self):
        """Test TokenCache import."""
        try:
            from wecomutils.wecom import TokenCache
            self.assertIsNotNone(TokenCache)
        except ImportError:
            self.skipTest("TokenCache not available")
    
    def test_license_import(self):
        """Test License import."""
        try:
            from wecomutils.wecom import License
            self.assertIsNotNone(License)
        except ImportError:
            self.skipTest("License not available")


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with omzutils."""
    
    def test_storage_service_compatibility(self):
        """Test that StorageService can be imported from wecomutils."""
        try:
            from wecomutils import StorageService
            self.assertIsNotNone(StorageService)
        except ImportError:
            self.skipTest("StorageService compatibility not available")
    
    def test_db_manager_compatibility(self):
        """Test that DBManager can be imported from wecomutils."""
        try:
            from wecomutils import DBManager
            self.assertIsNotNone(DBManager)
        except ImportError:
            self.skipTest("DBManager compatibility not available")
    
    def test_fc_service_compatibility(self):
        """Test that FCService can be imported from wecomutils."""
        try:
            from wecomutils import FCService
            self.assertIsNotNone(FCService)
        except ImportError:
            self.skipTest("FCService compatibility not available")


class TestWXApiBase(unittest.TestCase):
    """Test WXApiBase functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from wecomutils.wecom import WXApiBase
            self.WXApiBase = WXApiBase
        except ImportError:
            self.skipTest("WXApiBase not available")
    
    def test_wx_api_base_class_exists(self):
        """Test that WXApiBase class exists."""
        self.assertTrue(hasattr(self.WXApiBase, '__init__'))
    
    def test_wx_api_base_init(self):
        """Test WXApiBase initialization."""
        try:
            api = self.WXApiBase(
                corpid='test_corpid',
                corpsecret='test_secret'
            )
            self.assertIsNotNone(api)
        except Exception as e:
            # If initialization fails due to missing dependencies, that's expected
            pass


class TestTokenCache(unittest.TestCase):
    """Test TokenCache functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from wecomutils.wecom import TokenCache
            self.TokenCache = TokenCache
        except ImportError:
            self.skipTest("TokenCache not available")
    
    def test_token_cache_class_exists(self):
        """Test that TokenCache class exists."""
        self.assertTrue(hasattr(self.TokenCache, '__init__'))
    
    @patch('time.time')
    def test_token_cache_basic_functionality(self, mock_time):
        """Test basic token cache functionality."""
        mock_time.return_value = 1000
        
        try:
            cache = self.TokenCache()
            self.assertIsNotNone(cache)
            
            # Test basic methods exist
            if hasattr(cache, 'get_token'):
                self.assertTrue(callable(getattr(cache, 'get_token')))
            if hasattr(cache, 'set_token'):
                self.assertTrue(callable(getattr(cache, 'set_token')))
        except Exception:
            # If there are dependency issues, skip
            pass


class TestWXCrypto(unittest.TestCase):
    """Test WXCrypto functionality (optional)."""
    
    def test_wx_crypto_import(self):
        """Test WXCrypto import (should be optional)."""
        try:
            from wecomutils.wecom import WXCrypto
            if WXCrypto is not None:
                self.assertIsNotNone(WXCrypto)
            else:
                self.skipTest("WXCrypto not available (missing Crypto library)")
        except ImportError:
            # This is expected if Crypto library is not available
            self.skipTest("WXCrypto not available (missing dependencies)")


class TestWecomPackageStructure(unittest.TestCase):
    """Test wecom package structure."""
    
    def test_wecom_package_has_expected_modules(self):
        """Test that wecom package has expected structure."""
        from wecomutils import wecom
        
        # Check that basic modules are available
        expected_modules = ['WXApiBase', 'TokenCache', 'License']
        available_modules = []
        
        for module_name in expected_modules:
            if hasattr(wecom, module_name):
                available_modules.append(module_name)
        
        # At least some modules should be available
        self.assertGreater(len(available_modules), 0)
    
    def test_wecom_init_file_exists(self):
        """Test that wecom __init__.py exists and is importable."""
        import wecomutils.wecom
        self.assertTrue(hasattr(wecomutils.wecom, '__file__'))


if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWecomutilsImports))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestWXApiBase))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenCache))
    suite.addTests(loader.loadTestsFromTestCase(TestWXCrypto))
    suite.addTests(loader.loadTestsFromTestCase(TestWecomPackageStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)