"""性能测试模块"""

import time
import psutil
import functools
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    execution_time: float
    memory_usage_mb: float
    cpu_percent: float
    function_name: str
    args_count: int
    kwargs_count: int


class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.metrics: Dict[str, list[PerformanceMetrics]] = {}
    
    def profile(self, func: Callable) -> Callable:
        """性能分析装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 记录开始状态
            start_time = time.perf_counter()
            process = psutil.Process()
            start_memory = process.memory_info().rss / 1024 / 1024  # MB
            start_cpu = process.cpu_percent()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # 记录结束状态
                end_time = time.perf_counter()
                end_memory = process.memory_info().rss / 1024 / 1024  # MB
                end_cpu = process.cpu_percent()
                
                # 计算指标
                metrics = PerformanceMetrics(
                    execution_time=end_time - start_time,
                    memory_usage_mb=end_memory - start_memory,
                    cpu_percent=end_cpu - start_cpu,
                    function_name=func.__name__,
                    args_count=len(args),
                    kwargs_count=len(kwargs)
                )
                
                # 存储指标
                if func.__name__ not in self.metrics:
                    self.metrics[func.__name__] = []
                self.metrics[func.__name__].append(metrics)
        
        return wrapper
    
    @contextmanager
    def measure_block(self, block_name: str):
        """测量代码块性能"""
        start_time = time.perf_counter()
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024
        
        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = process.memory_info().rss / 1024 / 1024
            
            metrics = PerformanceMetrics(
                execution_time=end_time - start_time,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=0.0,  # 代码块测量不包含CPU
                function_name=block_name,
                args_count=0,
                kwargs_count=0
            )
            
            if block_name not in self.metrics:
                self.metrics[block_name] = []
            self.metrics[block_name].append(metrics)
    
    def get_stats(self, function_name: Optional[str] = None) -> Dict[str, Any]:
        """获取性能统计信息"""
        if function_name:
            if function_name not in self.metrics:
                return {}
            
            metrics_list = self.metrics[function_name]
        else:
            # 返回所有函数的统计
            all_stats = {}
            for fname in self.metrics:
                all_stats[fname] = self.get_stats(fname)
            return all_stats
        
        if not metrics_list:
            return {}
        
        execution_times = [m.execution_time for m in metrics_list]
        memory_usages = [m.memory_usage_mb for m in metrics_list]
        
        return {
            'call_count': len(metrics_list),
            'avg_execution_time': sum(execution_times) / len(execution_times),
            'min_execution_time': min(execution_times),
            'max_execution_time': max(execution_times),
            'avg_memory_usage': sum(memory_usages) / len(memory_usages),
            'max_memory_usage': max(memory_usages),
            'total_execution_time': sum(execution_times)
        }
    
    def clear_metrics(self, function_name: Optional[str] = None) -> None:
        """清除性能指标"""
        if function_name:
            self.metrics.pop(function_name, None)
        else:
            self.metrics.clear()
    
    def print_report(self, function_name: Optional[str] = None) -> None:
        """打印性能报告"""
        stats = self.get_stats(function_name)
        
        if function_name:
            if not stats:
                print(f"No metrics found for function: {function_name}")
                return
            
            print(f"\n=== Performance Report for {function_name} ===")
            print(f"Call Count: {stats['call_count']}")
            print(f"Average Execution Time: {stats['avg_execution_time']:.4f}s")
            print(f"Min/Max Execution Time: {stats['min_execution_time']:.4f}s / {stats['max_execution_time']:.4f}s")
            print(f"Average Memory Usage: {stats['avg_memory_usage']:.2f}MB")
            print(f"Max Memory Usage: {stats['max_memory_usage']:.2f}MB")
            print(f"Total Execution Time: {stats['total_execution_time']:.4f}s")
        else:
            print("\n=== Overall Performance Report ===")
            for fname, fstats in stats.items():
                if fstats:  # 只显示有数据的函数
                    print(f"\n{fname}:")
                    print(f"  Calls: {fstats['call_count']}")
                    print(f"  Avg Time: {fstats['avg_execution_time']:.4f}s")
                    print(f"  Total Time: {fstats['total_execution_time']:.4f}s")


# 全局性能分析器实例
profiler = PerformanceProfiler()


def benchmark(iterations: int = 1000):
    """基准测试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            print(f"\n🚀 Running benchmark for {func.__name__} ({iterations} iterations)")
            
            # 预热
            for _ in range(min(10, iterations // 10)):
                func(*args, **kwargs)
            
            # 基准测试
            start_time = time.perf_counter()
            for _ in range(iterations):
                result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            total_time = end_time - start_time
            avg_time = total_time / iterations
            
            print(f"📊 Benchmark Results:")
            print(f"   Total Time: {total_time:.4f}s")
            print(f"   Average Time: {avg_time:.6f}s")
            print(f"   Operations/sec: {iterations/total_time:.2f}")
            
            return result
        
        return wrapper
    return decorator