"""配置管理模块"""

from __future__ import annotations

import os
import json
from typing import Any, Dict, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field

from .exceptions import ConfigurationError


@dataclass
class StorageConfig:
    """存储配置"""
    base_path: str = field(default_factory=lambda: os.environ.get('STORAGE_PATH', str(Path.home() / '.omzutils' / 'storage')))
    encoding: str = 'utf-8'
    create_dirs: bool = True
    
    def __post_init__(self):
        if self.create_dirs:
            try:
                Path(self.base_path).mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError):
                # 如果无法创建目录，使用临时目录
                import tempfile
                self.base_path = tempfile.mkdtemp(prefix='omzutils_')


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = field(default_factory=lambda: os.environ.get('DB_HOST', 'localhost'))
    port: int = field(default_factory=lambda: int(os.environ.get('DB_PORT', '3306')))
    username: str = field(default_factory=lambda: os.environ.get('DB_USERNAME', ''))
    password: str = field(default_factory=lambda: os.environ.get('DB_PASSWORD', ''))
    database: str = field(default_factory=lambda: os.environ.get('DB_NAME', ''))
    charset: str = 'utf8mb4'
    pool_size: int = 5
    
    def get_connection_string(self) -> str:
        """获取数据库连接字符串"""
        if not all([self.host, self.username, self.database]):
            raise ConfigurationError("Database configuration incomplete")
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class FunctionComputeConfig:
    """函数计算配置"""
    endpoint: str = field(default_factory=lambda: os.environ.get('FC_ENDPOINT', ''))
    access_key_id: str = field(default_factory=lambda: os.environ.get('FC_ACCESS_KEY_ID', ''))
    access_key_secret: str = field(default_factory=lambda: os.environ.get('FC_ACCESS_KEY_SECRET', ''))
    region: str = field(default_factory=lambda: os.environ.get('FC_REGION', 'cn-hangzhou'))
    timeout: int = 30
    
    def validate(self) -> None:
        """验证配置完整性"""
        if not all([self.endpoint, self.access_key_id, self.access_key_secret]):
            raise ConfigurationError("Function Compute configuration incomplete")


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._config_cache: Dict[str, Any] = {}
        
        # 默认配置
        self.storage = StorageConfig()
        self.database = DatabaseConfig()
        self.function_compute = FunctionComputeConfig()
        
        # 如果指定了配置文件，则加载
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str) -> None:
        """从文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 更新存储配置
            if 'storage' in config_data:
                storage_data = config_data['storage']
                self.storage = StorageConfig(**storage_data)
            
            # 更新数据库配置
            if 'database' in config_data:
                db_data = config_data['database']
                self.database = DatabaseConfig(**db_data)
            
            # 更新函数计算配置
            if 'function_compute' in config_data:
                fc_data = config_data['function_compute']
                self.function_compute = FunctionComputeConfig(**fc_data)
                
        except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
            raise ConfigurationError(f"Failed to load configuration from {config_file}: {str(e)}")
    
    def save_to_file(self, config_file: str) -> None:
        """保存配置到文件"""
        config_data = {
            'storage': {
                'base_path': self.storage.base_path,
                'encoding': self.storage.encoding,
                'create_dirs': self.storage.create_dirs
            },
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'username': self.database.username,
                'password': self.database.password,
                'database': self.database.database,
                'charset': self.database.charset,
                'pool_size': self.database.pool_size
            },
            'function_compute': {
                'endpoint': self.function_compute.endpoint,
                'access_key_id': self.function_compute.access_key_id,
                'access_key_secret': self.function_compute.access_key_secret,
                'region': self.function_compute.region,
                'timeout': self.function_compute.timeout
            }
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise ConfigurationError(f"Failed to save configuration to {config_file}: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config_cache.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self._config_cache[key] = value
    
    def validate_all(self) -> None:
        """验证所有配置"""
        try:
            self.function_compute.validate()
        except ConfigurationError:
            # 函数计算配置可选，验证失败不影响其他功能
            pass


# 全局配置实例
config = ConfigManager()