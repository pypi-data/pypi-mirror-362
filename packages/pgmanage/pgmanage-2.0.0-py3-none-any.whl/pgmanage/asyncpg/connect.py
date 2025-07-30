import logging
import os
import atexit
from typing import Optional
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)

class AsyncPgPool:
    _instance = None
    _pool: Optional[AsyncConnectionPool] = None
    _pool_ctx = None
    _atexit_registered = False  # 添加标志以确保只注册一次

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncPgPool, cls).__new__(cls)
        return cls._instance

    def __init__(self, conn_str: str = None,min_size=0,max_size=20,timeout=180):
        self.min_size = min_size
        self.max_size = max_size
        self.timeout = timeout
        if not hasattr(self, 'conn_str'):
            if conn_str is None:
                conn_str = os.environ.get("PGLINK_URL")
                if conn_str is None:
                    raise ValueError("数据库连接变量 PGLINK_URL 不存在")
            self.conn_str = conn_str
            # 确保 atexit 只注册一次
            if not AsyncPgPool._atexit_registered:
                atexit.register(self._cleanup)
                AsyncPgPool._atexit_registered = True

    async def __aenter__(self):
        """异步上下文管理器入口"""
        if self._pool is None:
            self._pool_ctx = AsyncConnectionPool(self.conn_str,min_size=self.min_size,max_size=self.max_size,timeout=self.timeout)
            self._pool = await self._pool_ctx.__aenter__()
            logger.info("数据库连接池已初始化")
        return self._pool

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()

    @classmethod
    async def initialize(cls, conn_str: str=None):
        """初始化数据库连接池"""
        instance = cls(conn_str)
        return await instance.__aenter__()

    @classmethod
    def get_pool(cls) -> Optional[AsyncConnectionPool]:
        """获取连接池实例"""
        return cls._pool

    @classmethod
    async def close(cls):
        """关闭连接池"""
        if cls._pool_ctx is not None:
            await cls._pool_ctx.__aexit__(None, None, None)
            cls._pool = None
            cls._pool_ctx = None
            logger.info("数据库连接池已关闭")

    @classmethod
    def _cleanup(cls):
        """退出时的清理函数"""
        import asyncio
        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # 如果没有事件循环，创建一个新的
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop.is_running():
                loop.create_task(cls.close())
            else:
                try:
                    loop.run_until_complete(cls.close())
                finally:
                    loop.close()
                    
        except Exception as e:
            logger.error(f"清理连接池时发生错误: {e}") 
