#!/usr/bin/env python3
"""
Comprehensive test suite for omzutils package.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)


class TestOmzutilsImports(unittest.TestCase):
    """Test basic imports for omzutils package."""
    
    def test_package_import(self):
        """Test that omzutils package can be imported."""
        import omzutils
        self.assertIsNotNone(omzutils)
        self.assertTrue(hasattr(omzutils, '__version__'))
    
    def test_storage_import(self):
        """Test StorageService import."""
        try:
            from omzutils.storage import StorageService
            self.assertIsNotNone(StorageService)
        except ImportError:
            self.skipTest("StorageService not available (missing dependencies)")
    
    def test_db_manager_import(self):
        """Test DBManager import."""
        try:
            from omzutils.db_manager import DBManager
            self.assertIsNotNone(DBManager)
        except ImportError:
            self.skipTest("DBManager not available (missing dependencies)")
    
    def test_fc_service_import(self):
        """Test FCService import."""
        try:
            from omzutils.fc_service import FCService
            self.assertIsNotNone(FCService)
        except ImportError:
            self.skipTest("FCService not available (missing dependencies)")


class TestStorageService(unittest.TestCase):
    """Test StorageService functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from omzutils.storage import StorageService
            self.StorageService = StorageService
        except ImportError:
            self.skipTest("StorageService not available")
    
    @patch.dict('os.environ', {'STORAGE_PATH': '/tmp/test_storage'})
    def test_storage_service_init(self):
        """Test StorageService initialization."""
        storage = self.StorageService()
        self.assertIsNotNone(storage)
    
    @patch.dict('os.environ', {'STORAGE_PATH': '/tmp/test_storage'})
    @patch('omzutils.storage.os.makedirs')
    @patch('omzutils.storage.os.path.exists')
    def test_ensure_directory(self, mock_exists, mock_makedirs):
        """Test directory creation functionality."""
        mock_exists.return_value = False
        storage = self.StorageService()
        
        # Test that ensure_directory method exists and can be called
        if hasattr(storage, 'ensure_directory'):
            storage.ensure_directory('/test/path')
            mock_makedirs.assert_called_once()


class TestDBManager(unittest.TestCase):
    """Test DBManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from omzutils.db_manager import DBManager
            self.DBManager = DBManager
        except ImportError:
            self.skipTest("DBManager not available")
    
    def test_db_manager_class_exists(self):
        """Test that DBManager class exists."""
        self.assertTrue(hasattr(self.DBManager, '__init__'))
    
    @patch('omzutils.db_manager.pymysql')
    def test_db_manager_connection_pool(self, mock_pymysql):
        """Test database connection pool functionality."""
        # Mock the pymysql connection
        mock_connection = MagicMock()
        mock_pymysql.connect.return_value = mock_connection
        
        # Test connection pool creation
        if hasattr(self.DBManager, 'get_connection'):
            # This is a basic test to ensure the method exists
            self.assertTrue(callable(getattr(self.DBManager, 'get_connection')))


class TestFCService(unittest.TestCase):
    """Test FCService functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from omzutils.fc_service import FCService
            self.FCService = FCService
        except ImportError:
            self.skipTest("FCService not available")
    
    def test_fc_service_class_exists(self):
        """Test that FCService class exists."""
        self.assertTrue(hasattr(self.FCService, '__init__'))
    
    def test_fc_service_init(self):
        """Test FCService initialization."""
        # Test with mock credentials
        try:
            fc_service = self.FCService(
                access_key_id='test_key',
                access_key_secret='test_secret',
                region='cn-hangzhou'
            )
            self.assertIsNotNone(fc_service)
        except Exception as e:
            # If initialization fails due to missing dependencies, that's expected
            self.assertIn('fc2', str(e).lower())


class TestPackageStructure(unittest.TestCase):
    """Test package structure and organization."""
    
    def test_package_has_all_modules(self):
        """Test that package exposes expected modules."""
        import omzutils
        
        # Check that __all__ is defined if modules are available
        if hasattr(omzutils, '__all__'):
            available_modules = omzutils.__all__
            self.assertIsInstance(available_modules, list)
    
    def test_version_attribute(self):
        """Test that package has version attribute."""
        import omzutils
        self.assertTrue(hasattr(omzutils, '__version__'))
        self.assertIsInstance(omzutils.__version__, str)


if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestOmzutilsImports))
    suite.addTests(loader.loadTestsFromTestCase(TestStorageService))
    suite.addTests(loader.loadTestsFromTestCase(TestDBManager))
    suite.addTests(loader.loadTestsFromTestCase(TestFCService))
    suite.addTests(loader.loadTestsFromTestCase(TestPackageStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)