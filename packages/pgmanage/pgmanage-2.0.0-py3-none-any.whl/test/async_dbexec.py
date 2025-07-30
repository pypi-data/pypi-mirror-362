
import sys,os
sys.path.append(os.getcwd())


import logging
import asyncio
from pgmanage import AsyncPgExec

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 使用示例
async def main():
    import os
    DBURI = os.environ.get("PGLINK_URL")
    
    # 方式1：使用上下文管理器（推荐）
    async with AsyncPgExec(DBURI) as dbmange:
        # 生成测试数据
        data_to_bulk_insert = [
            {'id': f'{i}', 'name': f'name{i}88', 'age': i % 100, 
             'email': f'email{i}@example.com', 'fasle': True,'测试':f'ce-{i}'}
            for i in range(100000)
        ]

        result = await dbmange.upsert_data(
            'data_test', 'table_tEst', data_to_bulk_insert,
            batch_size=10000, update=True, create=True, add_columns=False,only_column=True
        )
        
        logger.info(f"总共成功插入或更新了 {result} 条记录")


    # 方式2：直接使用（程序结束时会自动关闭连接池）
    # 生成测试数据
    data_to_bulk_insert = [
        {'id': f'{i}', 'name': f'name{i}88', 'age': i % 100, 
         'email': f'email{i}@example.com', 'fasle': True,'平均支付_签收时长(秒)':90,'签收时长(秒)':33}
        for i in range(100000)
    ]
    db_exec = AsyncPgExec(DBURI)
    db_exec.pool = await db_exec.async_pool.initialize()
    result = await db_exec.upsert_data(
        'data_test', 'table_tEst', data_to_bulk_insert,
        batch_size=None, update=True, create=True, add_columns=False
    )
    logger.info(f"总共成功插入或更新了 {result} 条记录")
    # 不需要手动关闭，atexit 会处理

if __name__ == "__main__":
    asyncio.run(main())
