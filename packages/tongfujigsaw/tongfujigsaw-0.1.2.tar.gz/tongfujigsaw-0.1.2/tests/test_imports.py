#!/usr/bin/env python3
"""
Simple import test for wecomutils and omzutils packages.
"""

import sys
import os

# Add project root to path if running directly
if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, src_path)

try:
    # Test basic imports
    print("Testing basic imports...")
    
    # Test wecomutils package
    import wecomutils
    print(f"✓ Successfully imported wecomutils from: {wecomutils.__file__}")
    
    # Test omzutils package
    import omzutils
    print(f"✓ Successfully imported omzutils from: {omzutils.__file__}")
    
    # Test individual modules
    from omzutils.storage import StorageService
    print("✓ Successfully imported StorageService")
    
    # Test wecom subpackage
    from wecomutils.wecom import WXApiBase
    print("✓ Successfully imported WXApiBase")
    
    # Test backward compatibility
    try:
        from wecomutils import StorageService as StorageServiceCompat
        print("✓ Backward compatibility test: SUCCESS")
    except ImportError as e:
        print(f"⚠ Backward compatibility test: {str(e)}")
    
    print("\n🎉 All basic imports successful!")
    print("\nPackage structure:")
    print("├── omzutils/")
    print("│   ├── db_manager.py")
    print("│   ├── fc_service.py")
    print("│   └── storage.py")
    print("└── wecomutils/")
    print("    └── wecom/")

except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    sys.exit(1)

if __name__ == "__main__":
    print("\n✅ Test completed successfully!")