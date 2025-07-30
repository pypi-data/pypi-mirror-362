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

with dbm.pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        data = cur.fetchone()
        print("查询结果:",data)
        
with dbm.pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        data = cur.fetchone()
        print("查询结果:",data)