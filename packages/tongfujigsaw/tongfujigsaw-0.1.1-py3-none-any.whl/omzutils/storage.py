from __future__ import annotations

import os
import json
import logging
from typing import Any, Union, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class StorageService:
    """文件存储服务类，提供文件读写功能"""
    
    def __init__(self, base_path: Optional[str] = None) -> None:
        """初始化存储服务
        
        Args:
            base_path: 基础存储路径，如果为None则使用环境变量STORAGE_PATH或默认路径
        """
        self.base_path = base_path or os.environ.get('STORAGE_PATH', '/mnt/app')
        # 确保基础目录存在
        Path(self.base_path).mkdir(parents=True, exist_ok=True)

    def save_to_file(self, filename: str, content: Union[dict, list, str, Any]) -> None:
        """保存内容到文件
        
        Args:
            filename: 文件名
            content: 要保存的内容，支持字典、列表或字符串
            
        Raises:
            OSError: 文件操作失败
            json.JSONEncodeError: JSON序列化失败
        """
        filepath = Path(self.base_path) / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(content))
            logger.info(f"Successfully saved to {filepath}")
        except (OSError, json.JSONEncodeError) as e:
            logger.error(f"Failed to save to {filepath}: {str(e)}")
            raise

    def load_from_file(self, filename: str) -> Optional[Union[dict, list, str]]:
        """从文件加载内容
        
        Args:
            filename: 文件名
            
        Returns:
            文件内容，如果是JSON格式则返回解析后的对象，否则返回字符串
            如果文件不存在或读取失败则返回None
        """
        filepath = Path(self.base_path) / filename
        
        try:
            if not filepath.exists():
                return None
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content
        except OSError as e:
            logger.error(f"Failed to load from {filepath}: {str(e)}")
            return None