#!/usr/bin/env python3
"""
Simple test script for wecomutils and omzutils packages.
"""

import sys
import os

# Add project root to path if running directly
if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, src_path)

try:
    # Test wecomutils package
    import wecomutils
    print(f"Successfully imported wecomutils from: {wecomutils.__file__}")
    
    # Test omzutils package
    import omzutils
    from omzutils.db_manager import DBManager
    print(f"Successfully imported omzutils from: {omzutils.__file__}")
    
    # Test database functionality
    try:
        # Replace with actual test parameters appropriate for your setup
        result = DBManager.execute_query("SELECT 1")
        print(f"Database query test result: {result}")
    except Exception as e:
        print(f"Database test error: {str(e)}")
    
    # Test backward compatibility
    try:
        from wecomutils import DBManager as DBManagerCompat
        print("Backward compatibility test: SUCCESS")
    except ImportError as e:
        print(f"Backward compatibility test: {str(e)}")
    
    # Test other components
    from omzutils.storage import StorageService
    storage = StorageService()
    print(f"Storage service initialized: {storage}")
    
    print("All imports successful!")

except ImportError as e:
    print(f"Import error: {str(e)}")
    print("Make sure the package is installed or in your PYTHONPATH")
    sys.exit(1)

if __name__ == "__main__":
    print("Test completed!")