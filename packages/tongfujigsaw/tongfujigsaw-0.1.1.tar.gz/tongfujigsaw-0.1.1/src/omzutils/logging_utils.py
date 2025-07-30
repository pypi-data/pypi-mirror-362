"""统一日志系统"""

from __future__ import annotations

import logging
import sys
import json
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """结构化日志格式器"""
    
    def format(self, record: logging.LogRecord) -> str:
        # 基础日志信息
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # 添加自定义字段
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)


class OMZLogger:
    """OMZUtils 统一日志器"""
    
    def __init__(self, name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """设置日志处理器"""
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 简洁的控制台格式
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        self.logger.addHandler(console_handler)
        
        # 文件处理器（如果指定了日志目录）
        log_dir = Path.cwd() / 'logs'
        if log_dir.exists() or self._should_create_log_dir():
            self._setup_file_handler(log_dir)
    
    def _should_create_log_dir(self) -> bool:
        """判断是否应该创建日志目录"""
        # 在生产环境或明确指定时创建
        import os
        return os.environ.get('OMZ_CREATE_LOGS', '').lower() in ('true', '1', 'yes')
    
    def _setup_file_handler(self, log_dir: Path) -> None:
        """设置文件日志处理器"""
        log_dir.mkdir(exist_ok=True)
        
        # 详细的文件日志
        file_handler = logging.FileHandler(
            log_dir / f'{self.logger.name}.log',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 结构化格式用于文件
        file_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **extra_data) -> None:
        """调试日志"""
        self._log(logging.DEBUG, message, extra_data)
    
    def info(self, message: str, **extra_data) -> None:
        """信息日志"""
        self._log(logging.INFO, message, extra_data)
    
    def warning(self, message: str, **extra_data) -> None:
        """警告日志"""
        self._log(logging.WARNING, message, extra_data)
    
    def error(self, message: str, **extra_data) -> None:
        """错误日志"""
        self._log(logging.ERROR, message, extra_data)
    
    def critical(self, message: str, **extra_data) -> None:
        """严重错误日志"""
        self._log(logging.CRITICAL, message, extra_data)
    
    def _log(self, level: int, message: str, extra_data: Dict[str, Any]) -> None:
        """内部日志方法"""
        if extra_data:
            # 创建带有额外数据的日志记录
            record = self.logger.makeRecord(
                self.logger.name, level, '', 0, message, (), None
            )
            record.extra_data = extra_data
            self.logger.handle(record)
        else:
            self.logger.log(level, message)
    
    def log_function_call(self, func_name: str, args: tuple = (), kwargs: dict = None) -> None:
        """记录函数调用"""
        self.debug(
            f"Function call: {func_name}",
            function=func_name,
            args_count=len(args),
            kwargs_keys=list(kwargs.keys()) if kwargs else []
        )
    
    def log_performance(self, operation: str, duration: float, **metrics) -> None:
        """记录性能指标"""
        self.info(
            f"Performance: {operation} completed in {duration:.4f}s",
            operation=operation,
            duration=duration,
            **metrics
        )
    
    def log_error_with_context(self, error: Exception, context: str, **extra_data) -> None:
        """记录带上下文的错误"""
        self.error(
            f"Error in {context}: {str(error)}",
            error_type=type(error).__name__,
            context=context,
            **extra_data,
            exc_info=True
        )


def get_logger(name: str, level: str = 'INFO') -> OMZLogger:
    """获取日志器实例"""
    return OMZLogger(name, level)


# 预定义的日志器
storage_logger = get_logger('omzutils.storage')
db_logger = get_logger('omzutils.database')
fc_logger = get_logger('omzutils.function_compute')
performance_logger = get_logger('omzutils.performance')


def log_execution_time(logger: Optional[OMZLogger] = None):
    """执行时间记录装饰器"""
    def decorator(func):
        import functools
        import time
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            log = logger or get_logger(func.__module__)
            
            try:
                log.log_function_call(func.__name__, args, kwargs)
                result = func(*args, **kwargs)
                
                duration = time.perf_counter() - start_time
                log.log_performance(func.__name__, duration)
                
                return result
            except Exception as e:
                duration = time.perf_counter() - start_time
                log.log_error_with_context(
                    e, 
                    f"function {func.__name__}",
                    duration=duration
                )
                raise
        
        return wrapper
    return decorator