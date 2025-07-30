# test.py

import os
import sys
sys.path.append(os.getcwd())  # 确保可以从当前目录导入模块

# 设置日志
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import asyncio
from pgmanage import AsyncPgPool
async def main():
    try:
        # 初始化连接池
        pool = await AsyncPgPool.initialize()

        # 使用连接池执行数据库操作
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
                rows = await cur.fetchall()
                for row in rows:
                    print("查询结果:",row)
    except Exception as e:
        logger.error(f"发生错误: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())