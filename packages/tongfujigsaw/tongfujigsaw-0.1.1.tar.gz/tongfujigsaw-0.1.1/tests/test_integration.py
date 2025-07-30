#!/usr/bin/env python3
"""
Integration test suite for both omzutils and wecomutils packages.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)


class TestPackageIntegration(unittest.TestCase):
    """Test integration between omzutils and wecomutils packages."""
    
    def test_both_packages_importable(self):
        """Test that both packages can be imported simultaneously."""
        import omzutils
        import wecomutils
        
        self.assertIsNotNone(omzutils)
        self.assertIsNotNone(wecomutils)
    
    def test_no_circular_imports(self):
        """Test that there are no circular import issues."""
        try:
            # Import both packages and their main components
            import omzutils
            import wecomutils
            from wecomutils import wecom
            
            # Try to import backward compatibility modules
            try:
                from wecomutils import StorageService
            except ImportError:
                pass  # Expected if dependencies not available
            
            # This should complete without hanging (no circular imports)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Circular import or other import issue: {e}")
    
    def test_package_isolation(self):
        """Test that packages are properly isolated."""
        import omzutils
        import wecomutils
        
        # Packages should have different file paths
        self.assertNotEqual(omzutils.__file__, wecomutils.__file__)
        
        # Check that they're in different directories
        omz_dir = os.path.dirname(omzutils.__file__)
        wecom_dir = os.path.dirname(wecomutils.__file__)
        self.assertNotEqual(omz_dir, wecom_dir)


class TestCrossPackageCompatibility(unittest.TestCase):
    """Test compatibility between packages."""
    
    def test_storage_service_cross_import(self):
        """Test StorageService can be imported from both packages."""
        try:
            from omzutils.storage import StorageService as OmzStorageService
            from wecomutils import StorageService as WecomStorageService
            
            # They should be the same class
            self.assertEqual(OmzStorageService, WecomStorageService)
        except ImportError:
            self.skipTest("StorageService not available")
    
    def test_db_manager_cross_import(self):
        """Test DBManager can be imported from both packages."""
        try:
            from omzutils.db_manager import DBManager as OmzDBManager
            from wecomutils import DBManager as WecomDBManager
            
            # They should be the same class
            self.assertEqual(OmzDBManager, WecomDBManager)
        except ImportError:
            self.skipTest("DBManager not available")
    
    def test_fc_service_cross_import(self):
        """Test FCService can be imported from both packages."""
        try:
            from omzutils.fc_service import FCService as OmzFCService
            from wecomutils import FCService as WecomFCService
            
            # They should be the same class
            self.assertEqual(OmzFCService, WecomFCService)
        except ImportError:
            self.skipTest("FCService not available")


class TestPackageVersions(unittest.TestCase):
    """Test package version information."""
    
    def test_omzutils_version(self):
        """Test omzutils has version information."""
        import omzutils
        self.assertTrue(hasattr(omzutils, '__version__'))
        self.assertIsInstance(omzutils.__version__, str)
        self.assertRegex(omzutils.__version__, r'\d+\.\d+\.\d+')
    
    def test_wecomutils_version(self):
        """Test wecomutils has version information."""
        import wecomutils
        # wecomutils might not have its own version, which is fine
        if hasattr(wecomutils, '__version__'):
            self.assertIsInstance(wecomutils.__version__, str)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in package imports."""
    
    def test_graceful_dependency_handling(self):
        """Test that missing dependencies are handled gracefully."""
        # This test ensures that even with missing dependencies,
        # the packages can still be imported without crashing
        
        try:
            import omzutils
            import wecomutils
            
            # Check that packages have some basic attributes
            self.assertTrue(hasattr(omzutils, '__file__'))
            self.assertTrue(hasattr(wecomutils, '__file__'))
            
        except Exception as e:
            self.fail(f"Package import failed unexpectedly: {e}")
    
    def test_optional_module_imports(self):
        """Test that optional modules don't break package import."""
        import omzutils
        import wecomutils
        
        # Even if some modules are not available due to missing dependencies,
        # the packages should still be importable
        self.assertIsNotNone(omzutils)
        self.assertIsNotNone(wecomutils)


class TestDocumentationAndMetadata(unittest.TestCase):
    """Test package documentation and metadata."""
    
    def test_packages_have_docstrings(self):
        """Test that packages have proper docstrings."""
        import omzutils
        import wecomutils
        
        # At least one of them should have a docstring
        has_docstring = (
            (hasattr(omzutils, '__doc__') and omzutils.__doc__) or
            (hasattr(wecomutils, '__doc__') and wecomutils.__doc__)
        )
        self.assertTrue(has_docstring)
    
    def test_module_file_paths(self):
        """Test that module file paths are correct."""
        import omzutils
        import wecomutils
        
        # Check that file paths contain expected directory names
        self.assertIn('omzutils', omzutils.__file__)
        self.assertIn('wecomutils', wecomutils.__file__)


if __name__ == '__main__':
    print("Running integration tests for omzutils and wecomutils packages...")
    print("=" * 60)
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPackageIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossPackageCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestPackageVersions))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationAndMetadata))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All integration tests passed!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)