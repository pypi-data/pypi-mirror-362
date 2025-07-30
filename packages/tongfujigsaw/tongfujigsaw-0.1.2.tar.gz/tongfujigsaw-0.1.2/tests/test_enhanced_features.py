"""测试新增的核心功能模块"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from omzutils.storage import StorageService
from omzutils.exceptions import OMZUtilsError, StorageError, handle_exception
from omzutils.config import ConfigManager, StorageConfig
from omzutils.logging_utils import get_logger
from omzutils.performance import profiler, benchmark


class TestStorageServiceEnhanced:
    """测试增强的存储服务"""
    
    def test_storage_with_custom_path(self):
        """测试自定义路径初始化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            assert storage.base_path == temp_dir
    
    def test_save_and_load_json(self):
        """测试JSON数据保存和加载"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            
            test_data = {"key": "value", "number": 42}
            storage.save_to_file("test.json", test_data)
            
            loaded_data = storage.load_from_file("test.json")
            assert loaded_data == test_data
    
    def test_save_and_load_text(self):
        """测试文本数据保存和加载"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            
            test_text = "Hello, World!"
            storage.save_to_file("test.txt", test_text)
            
            loaded_text = storage.load_from_file("test.txt")
            assert loaded_text == test_text
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            result = storage.load_from_file("nonexistent.txt")
            assert result is None
    
    def test_type_annotations(self):
        """测试类型注解是否正确"""
        storage = StorageService()
        
        # 这些调用应该通过类型检查
        storage.save_to_file("test.txt", "string")
        storage.save_to_file("test.json", {"key": "value"})
        storage.save_to_file("test.list", [1, 2, 3])
        
        result = storage.load_from_file("test.txt")
        assert isinstance(result, (str, dict, list, type(None)))


class TestExceptionHandling:
    """测试异常处理模块"""
    
    def test_omz_utils_error(self):
        """测试基础异常类"""
        error = OMZUtilsError("Test message", "TEST_CODE", {"detail": "value"})
        
        assert str(error) == "[TEST_CODE] Test message"
        assert error.error_code == "TEST_CODE"
        assert error.details == {"detail": "value"}
    
    def test_storage_error(self):
        """测试存储异常"""
        error = StorageError("Storage failed")
        assert isinstance(error, OMZUtilsError)
        assert str(error) == "Storage failed"
    
    def test_handle_exception_reraise(self):
        """测试异常处理函数重新抛出"""
        original_error = ValueError("Original error")
        
        with pytest.raises(OMZUtilsError) as exc_info:
            handle_exception(original_error, "Test context")
        
        assert "Test context: Original error" in str(exc_info.value)
        assert exc_info.value.error_code == "UNEXPECTED_ERROR"


class TestConfigManager:
    """测试配置管理器"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ConfigManager()
        
        assert isinstance(config.storage, StorageConfig)
        assert config.storage.encoding == 'utf-8'
        assert config.storage.create_dirs is True
    
    def test_config_from_file(self):
        """测试从文件加载配置"""
        config_data = {
            "storage": {
                "base_path": "/custom/path",
                "encoding": "utf-16"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config = ConfigManager(config_file)
            assert config.storage.base_path == "/custom/path"
            assert config.storage.encoding == "utf-16"
        finally:
            Path(config_file).unlink()
    
    def test_config_cache(self):
        """测试配置缓存功能"""
        config = ConfigManager()
        
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
        assert config.get("nonexistent", "default") == "default"


class TestLoggingUtils:
    """测试日志工具"""
    
    def test_get_logger(self):
        """测试获取日志器"""
        logger = get_logger("test_logger")
        assert logger.logger.name == "test_logger"
    
    def test_structured_logging(self):
        """测试结构化日志"""
        logger = get_logger("test_structured")
        
        # 这些调用应该不会抛出异常
        logger.info("Test message", extra_field="extra_value")
        logger.error("Error message", error_code="E001")
        logger.log_performance("test_operation", 0.123, records_processed=100)


class TestPerformanceProfiler:
    """测试性能分析器"""
    
    def test_profile_decorator(self):
        """测试性能分析装饰器"""
        @profiler.profile
        def test_function(x, y):
            return x + y
        
        result = test_function(1, 2)
        assert result == 3
        
        stats = profiler.get_stats("test_function")
        assert stats['call_count'] == 1
        assert 'avg_execution_time' in stats
    
    def test_measure_block(self):
        """测试代码块测量"""
        with profiler.measure_block("test_block"):
            sum(range(1000))
        
        stats = profiler.get_stats("test_block")
        assert stats['call_count'] == 1
    
    def test_benchmark_decorator(self):
        """测试基准测试装饰器"""
        @benchmark(iterations=10)
        def simple_function():
            return sum(range(100))
        
        # 这应该运行基准测试并返回结果
        result = simple_function()
        assert result == sum(range(100))
    
    def test_clear_metrics(self):
        """测试清除指标"""
        @profiler.profile
        def temp_function():
            pass
        
        temp_function()
        assert profiler.get_stats("temp_function")['call_count'] == 1
        
        profiler.clear_metrics("temp_function")
        assert profiler.get_stats("temp_function") == {}


class TestIntegration:
    """集成测试"""
    
    def test_storage_with_logging(self):
        """测试存储服务与日志集成"""
        logger = get_logger("integration_test")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            
            # 使用日志记录存储操作
            logger.info("Starting storage test")
            storage.save_to_file("integration.json", {"test": "data"})
            
            data = storage.load_from_file("integration.json")
            assert data == {"test": "data"}
            
            logger.info("Storage test completed", records_saved=1)
    
    def test_performance_with_storage(self):
        """测试存储操作的性能分析"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = StorageService(base_path=temp_dir)
            
            @profiler.profile
            def save_multiple_files():
                for i in range(10):
                    storage.save_to_file(f"file_{i}.json", {"index": i})
            
            save_multiple_files()
            
            stats = profiler.get_stats("save_multiple_files")
            assert stats['call_count'] == 1
            assert stats['avg_execution_time'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])