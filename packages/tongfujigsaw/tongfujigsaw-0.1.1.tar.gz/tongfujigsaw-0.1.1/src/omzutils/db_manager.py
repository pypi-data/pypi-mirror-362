import pymysql
import logging
from dbutils.pooled_db import PooledDB
import threading
import os

# 配置日志
logger = logging.getLogger(__name__)

class DBManager:
    """数据库连接管理器，提供数据库连接和操作功能"""
    
    # 数据库连接参数
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'db_host.com'),
        'user': os.environ.get('DB_USER', 'db_user'),
        'password': os.environ.get('DB_PASSWORD', 'db_password'),
        'database': os.environ.get('DB_NAME', 'db_name'),
        'charset': os.environ.get('DB_CHARSET', 'utf8mb4'),
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    # 连接池配置
    POOL_CONFIG = {
        'mincached': 5,      # 初始化时创建的连接数
        'maxcached': 20,     # 连接池中最多闲置的连接数
        'maxshared': 3,      # 连接池中最多共享的连接数
        'maxconnections': 100, # 连接池中最多允许的连接数
        'blocking': True,    # 连接池中如果没有可用连接后是否阻塞等待
        'maxusage': None,    # 一个连接最多被重复使用的次数，None表示无限制
        'setsession': [],    # 开始会话前执行的命令列表
        'ping': 0,           # ping MySQL服务端确保连接的存活
    }
    
    # 线程锁，用于确保线程安全
    _lock = threading.Lock()
    
    # 连接池实例
    _pool = None
    
    @classmethod
    def _get_pool(cls):
        """获取连接池实例（单例模式）"""
        if cls._pool is None:
            with cls._lock:
                if cls._pool is None:
                    logger.info("初始化数据库连接池")
                    cls._pool = PooledDB(
                        creator=pymysql,
                        **cls.DB_CONFIG,
                        **cls.POOL_CONFIG
                    )
        return cls._pool
    
    @classmethod
    def get_connection(cls):
        """从连接池获取数据库连接"""
        logger.debug("从连接池获取数据库连接")
        return cls._get_pool().connection()
    
    @classmethod
    def execute_query(cls, sql, params=None, fetch_all=True):
        """执行查询并返回结果"""
        conn = cls.get_connection()
        try:
            with conn.cursor() as cursor:
                logger.debug(f"执行SQL: {sql}, 参数: {params}")
                cursor.execute(sql, params or ())
                if fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                return result
        finally:
            conn.close()  # 将连接归还到连接池
            logger.debug("数据库连接已归还到连接池")
    
    @classmethod
    def execute_update(cls, sql, params=None):
        """执行更新操作（INSERT, UPDATE, DELETE）并返回影响的行数"""
        conn = cls.get_connection()
        try:
            with conn.cursor() as cursor:
                logger.debug(f"执行SQL: {sql}, 参数: {params}")
                affected_rows = cursor.execute(sql, params or ())
                conn.commit()
                return affected_rows
        except Exception as e:
            conn.rollback()
            logger.error(f"执行SQL出错: {str(e)}", exc_info=True)
            raise
        finally:
            conn.close()  # 将连接归还到连接池
            logger.debug("数据库连接已归还到连接池")
    
    @classmethod
    def execute_many(cls, sql, params_list):
        """批量执行SQL语句"""
        conn = cls.get_connection()
        try:
            with conn.cursor() as cursor:
                logger.debug(f"批量执行SQL: {sql}, 参数数量: {len(params_list)}")
                affected_rows = cursor.executemany(sql, params_list)
                conn.commit()
                return affected_rows
        except Exception as e:
            conn.rollback()
            logger.error(f"批量执行SQL出错: {str(e)}", exc_info=True)
            raise
        finally:
            conn.close()  # 将连接归还到连接池
            logger.debug("数据库连接已归还到连接池")
    
    @classmethod
    def close_pool(cls):
        """关闭连接池（通常在应用关闭时调用）"""
        if cls._pool is not None:
            with cls._lock:
                if cls._pool is not None:
                    logger.info("关闭数据库连接池")
                    cls._pool.close()
                    cls._pool = None 