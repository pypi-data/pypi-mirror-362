"""OMZUtils package for general utility functions."""

__version__ = "0.1.0"

# Core modules (no external dependencies)
from .storage import StorageService
from .exceptions import (
    OMZUtilsError, StorageError, DatabaseError, 
    FunctionComputeError, ConfigurationError,
    handle_exception, safe_execute
)
from .config import config, ConfigManager, StorageConfig, DatabaseConfig, FunctionComputeConfig
from .logging_utils import get_logger, log_execution_time
from .performance import profiler, benchmark

# Optional imports that require additional dependencies
_available_modules = ['StorageService', 'OMZUtilsError', 'ConfigManager', 'get_logger', 'profiler']

try:
    from .db_manager import DBManager
    _available_modules.append('DBManager')
except ImportError:
    pass

try:
    from .fc_service import FCService
    _available_modules.append('FCService')
except ImportError:
    pass

__all__ = _available_modules