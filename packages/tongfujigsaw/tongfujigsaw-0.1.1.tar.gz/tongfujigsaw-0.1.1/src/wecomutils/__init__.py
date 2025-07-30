"""wecomutils package for WeChat Work/WeCom integration."""

__version__ = "0.1.1"

# Import wecom subpackage
from . import wecom

# For backward compatibility, re-export omzutils functions
# try:
#     from omzutils.storage import StorageService
#     from omzutils.db_manager import DBManager
#     from omzutils.fc_service import FCService
    
#     __all__ = ['wecom', 'StorageService', 'DBManager', 'FCService']
# except ImportError:
    # If omzutils is not available, only export wecom
__all__ = ['wecom']