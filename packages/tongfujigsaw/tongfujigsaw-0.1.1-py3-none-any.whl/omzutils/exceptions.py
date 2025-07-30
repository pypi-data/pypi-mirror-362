"""统一异常处理模块"""

from __future__ import annotations

import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class OMZUtilsError(Exception):
    """OMZUtils 基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class StorageError(OMZUtilsError):
    """存储相关异常"""
    pass


class DatabaseError(OMZUtilsError):
    """数据库相关异常"""
    pass


class FunctionComputeError(OMZUtilsError):
    """函数计算相关异常"""
    pass


class ConfigurationError(OMZUtilsError):
    """配置相关异常"""
    pass


def handle_exception(
    exception: Exception,
    context: str,
    logger_instance: Optional[logging.Logger] = None,
    reraise: bool = True
) -> None:
    """统一异常处理函数
    
    Args:
        exception: 捕获的异常
        context: 异常发生的上下文描述
        logger_instance: 日志记录器，如果为None则使用默认logger
        reraise: 是否重新抛出异常
        
    Raises:
        重新抛出原异常或包装后的异常
    """
    log = logger_instance or logger
    
    error_msg = f"{context}: {str(exception)}"
    log.error(error_msg, exc_info=True)
    
    if reraise:
        if isinstance(exception, OMZUtilsError):
            raise
        else:
            # 将其他异常包装为 OMZUtilsError
            raise OMZUtilsError(
                message=error_msg,
                error_code="UNEXPECTED_ERROR",
                details={"original_exception": type(exception).__name__}
            ) from exception


def safe_execute(
    func: callable,
    *args,
    default_return: Any = None,
    context: str = "Function execution",
    logger_instance: Optional[logging.Logger] = None,
    **kwargs
) -> Any:
    """安全执行函数，捕获异常并返回默认值
    
    Args:
        func: 要执行的函数
        *args: 函数参数
        default_return: 异常时的默认返回值
        context: 执行上下文描述
        logger_instance: 日志记录器
        **kwargs: 函数关键字参数
        
    Returns:
        函数执行结果或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log = logger_instance or logger
        log.warning(f"{context} failed: {str(e)}")
        return default_return