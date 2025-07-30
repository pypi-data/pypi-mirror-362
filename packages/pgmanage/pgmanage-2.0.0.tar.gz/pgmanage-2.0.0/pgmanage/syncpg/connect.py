

import atexit
import os
from psycopg_pool import ConnectionPool
# 设置日志
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import platform
if platform.system() == 'Windows':
    import asyncio
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

class PgPool:
    def __init__(self, conn_str: str = None,min_size=0,max_size=20,timeout=180):
        if conn_str is None:
            conn_str = os.environ.get("PGLINK_URL")
            if conn_str is None:
                print("示例:dbname=mydb user=myuser password=mypassword host=myhost port=5432")
                raise ValueError("Database connection string not provided and PGLINK_URL environment variable not set.")
        
        try:
            self.pool = ConnectionPool(conninfo=conn_str,min_size=min_size,max_size=max_size,timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize database connection pool: {e}")
        
        atexit.register(self.close_pool)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_pool()

    def close_pool(self):
        if hasattr(self, 'pool') and self.pool is not None:
            try:
                self.pool.close()
                logger.info("运行完毕已自动关闭连接池")
            finally:
                self.pool = None