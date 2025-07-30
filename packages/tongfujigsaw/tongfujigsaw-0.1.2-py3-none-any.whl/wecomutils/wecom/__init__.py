# providersapp-ai-customerservice/code/services/wecom/__init__.py
"""
企业微信API模块

包含以下主要组件：
- WXApiBase: 基础API类
- WXApiInternal: 内部应用API
- WXApiProviderApp: 第三方应用API
- WXApiProviderDev: 代开发应用API
- LicenseModule: 许可证管理模块
"""

# Core imports that should always be available
from .token_cache import TokenCache

# Optional imports that require additional dependencies
__all__ = ['TokenCache']

# Try to import API classes that depend on requests
try:
    from .wx_api import WXApiBase
    __all__.append('WXApiBase')
except ImportError:
    WXApiBase = None

try:
    from .wx_api_internal import WXApiInternal
    __all__.append('WXApiInternal')
except ImportError:
    WXApiInternal = None

try:
    from .wx_api_providerapp import WXApiProviderApp
    __all__.append('WXApiProviderApp')
except ImportError:
    WXApiProviderApp = None

try:
    from .wx_api_providerdev import WXApiProviderDev
    __all__.append('WXApiProviderDev')
except ImportError:
    WXApiProviderDev = None

try:
    from .license import LicenseModule
    __all__.append('LicenseModule')
except ImportError:
    LicenseModule = None

# Try to import crypto functionality
try:
    from .wx_crypto import WXCrypto
    __all__.append('WXCrypto')
except ImportError:
    WXCrypto = None