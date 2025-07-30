import logging
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class PgPool:
    _instance = None
    _pool = None
    _conn_str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def init_pool(cls, conn_str: str):
        """初始化连接字符串"""
        cls._conn_str = conn_str

    @classmethod
    @asynccontextmanager
    async def get_pool(cls):
        """获取连接池的异步上下文管理器"""
        if cls._conn_str is None:
            raise ValueError("连接池未初始化，请先调用 init_pool(conn_str)")
            
        try:
            async with AsyncConnectionPool(cls._conn_str) as pool:
                yield pool
        except Exception as e:
            logger.error(f"连接池操作失败: {e}")
            raise 