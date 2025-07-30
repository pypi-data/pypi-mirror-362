
import sys,os
sys.path.append(os.getcwd())

## 同步使用示例

from pgmanage import PgPool

dbm = PgPool()
with dbm.pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        data = cur.fetchone()
        print("查询结果:",data)



# 异步使用示例

import asyncio
from pgmanage import AsyncPgPool

# async def test():
#     dbm =await DbmanagerAsync.connect()
#     async with dbm.pool.connection() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute("SELECT 1")
#             data = await cur.fetchone()
#             print(data)



# if __name__ == "__main__":
#     asyncio.run(test())
