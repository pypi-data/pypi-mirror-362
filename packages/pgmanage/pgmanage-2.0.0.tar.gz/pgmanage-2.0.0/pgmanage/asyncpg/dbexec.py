import sys,os
sys.path.append(os.getcwd())

import logging
from typing import Dict, List, Any, Optional
import asyncio
import datetime
from psycopg import sql


from pgmanage.asyncpg.connect import AsyncPgPool

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import platform
# if platform.system() == 'Windows':
#     import asyncio
#     from asyncio import WindowsSelectorEventLoopPolicy
#     asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

class AsyncPgExec:
    def __init__(self, conn_str: str = None,min_size=0,max_size=20,timeout=180):
        """
        初始化数据库连接配置。
        
        :param conn_str: 数据库连接字符串 'dbname=shop_data user=postgres password=xxxxx host=127.0.0.1 port=5432'
        :param min_size: 连接池最小连接数，默认为0
        :param max_size: 连接池最大连接数，默认为20
        :param timeout: 连接超时时间，默认为180秒
        """
        self.conn_str = conn_str
        self.pool = None
        self.async_pool = AsyncPgPool(conn_str,min_size=min_size,max_size=max_size,timeout=timeout)

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.pool = await self.async_pool.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.async_pool.__aexit__(exc_type, exc_val, exc_tb)

    async def _exec_query(self, query: str, params: Optional[List[Any]] = None) -> bool:
        """执行SQL查询，并处理异常"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    if params:
                        await cur.execute(query, params)
                    else:
                        await cur.execute(query)
                    await conn.commit()
                    return True
                except Exception as e:
                    await conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise

    async def exec_query(self, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """执行SQL查询，返回查询数据列表字典"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    if params:
                        await cur.execute(query, params)
                    else:
                        await cur.execute(query)
                    await conn.commit()
                    column_names = [desc[0] for desc in cur.description]
                    results = await cur.fetchall()
                    result_dicts = [dict(zip(column_names, row)) for row in results]
                    return result_dicts
                except Exception as e:
                    await conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise

    async def exec_query_rowcount(self, query: str, params: Optional[List[Any]] = None) -> int:
        """执行SQL查询，返回处理的数据行数"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    if params:
                        await cur.execute(query, params)
                    else:
                        await cur.execute(query)
                    await conn.commit()
                    return cur.rowcount
                except Exception as e:
                    await conn.rollback()
                    logger.error(f"查询执行失败: {e}")
                    raise

    def infer_data_type(self, value: Any) -> str:
        """
        根据传入的值推断数据类型。
        
        :param value: 要推断的数据值
        :return: 推断出的数据类型
        """
        # print(value,type(value))
        if isinstance(value, int) and not isinstance(value, bool):
            return 'INT'
        elif isinstance(value, float):
            return 'FLOAT'
        elif isinstance(value, bool):
            return 'BOOLEAN'
        elif isinstance(value, str):
            return 'VARCHAR'
        elif isinstance(value, list):
            return 'VARCHAR[]'  # PostgreSQL 数组类型
        elif isinstance(value, dict):
            return 'JSONB'  # PostgreSQL JSONB 类型
        elif isinstance(value, (datetime.date, datetime.datetime)):
            return 'TIMESTAMP'
        else:
            return 'VARCHAR'  # 默认类型

    async def check_table(self, schema: str, table: str) -> bool:
        """检查表是否存在"""
        # query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = %s AND table_name = %s);"

        # 使用 sql 模块构建安全的SQL查询
        query = sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = {schema} AND table_name = {table})").format(
            schema=sql.Literal(schema),
            table=sql.Literal(table)
        )

        async with self.pool.connection() as conn:
            # print(query.as_string(conn))   # 输出SQL查询
            async with conn.cursor() as cur:
                # await cur.execute(query, (schema, table))
                await cur.execute(query)
                exists = (await cur.fetchone())[0]
                if not exists:
                    logger.warning(f"表 '{schema}.{table}' 不存在")
                return exists

    async def create_table(self, schema: str, table: str, columns: Dict[str, str], primary_key: Optional[str] = None) -> None:
        """
        创建新表。
        
        :param schema: 模式名
        :param table: 表名
        :param columns: 列定义的字典，键为列名，值为列类型
        :param primary_key: 主键列名，默认为None
        """
        # cols_sql = ', '.join([f"{col} {ctype}" for col, ctype in columns.items()])
        # pk_sql = f", PRIMARY KEY ({primary_key})" if primary_key else ""
        # create_sql = f"CREATE TABLE {schema}.{table} ({cols_sql}{pk_sql});"

        # 构建列定义部分
        cols_sql = sql.SQL(', ').join(
            sql.SQL("{col} {ctype}").format(
                col=sql.Identifier(col),
                ctype=sql.SQL(ctype)
            ) for col, ctype in columns.items()
        )

        # 如果有主键，则添加PRIMARY KEY约束
        pk_sql = sql.SQL(", PRIMARY KEY ({pk})").format(pk=sql.Identifier(primary_key)) if primary_key else sql.SQL("")

        # 构建完整的CREATE TABLE语句
        create_sql = sql.SQL("CREATE TABLE {schema}.{table} ({cols}{pk});").format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            cols=cols_sql,
            pk=pk_sql
        )

        await self._exec_query(create_sql)
        logger.info(f"创建表 '{schema}.{table}' 成功")

    async def get_columns(self, schema: str, table: str) -> Dict[str, str]:
        """
        获取表的所有列及其数据类型。
        
        :param schema: 模式名
        :param table: 表名
        :return: 字典，键为列名，值为数据类型
        """
        query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s;"
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (schema, table))
                return {row[0]: row[1] for row in await cur.fetchall()}

    async def add_column(self, schema: str, table: str, column: str, column_type: str) -> None:
        """
        向表中添加一列。
        
        :param schema: 模式名
        :param table: 表名
        :param column: 新列名
        :param column_type: 新列的数据类型
        """
        # add_col_sql = f"ALTER TABLE {schema}.{table} ADD COLUMN {column} {column_type};"

        # 使用 sql 模块构建安全的SQL查询
        add_col_sql = sql.SQL("ALTER TABLE {schema}.{table} ADD COLUMN {column} {column_type};").format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            column=sql.Identifier(column),
            column_type=sql.SQL(column_type)  # 注意：这里假设 column_type 是一个有效的 SQL 类型名称
        )

        await self._exec_query(add_col_sql)
        logger.info(f"向表 '{schema}.{table}' 添加列 '{column}',类型 '{column_type}' 成功")

    async def upsert_batch(self, schema, table, batch, conflict_target, do_update_set, start_index, end_index):
        """
        执行单个批次的异步插入或更新
        :param schema: 模式名
        :param table: 表名
        :param batch: 要插入或更新的数据批次
        :param conflict_target: 冲突目标，例如：ON CONFLICT (id) DO UPDATE SET
        :param do_update_set: 更新设置，例如：id = EXCLUDED.id, name = EXCLUDED.name
        :param start_index: 批次起始索引
        :param end_index: 批次结束索引
        :return: 批次中更新的记录数
        """
        if not batch:
            return 0

        # columns = ', '.join(batch[0].keys())
        columns = sql.SQL(", ").join(sql.Identifier(col) for col in batch[0].keys())
        # placeholders = ', '.join(['(%s)' % ', '.join(['%s'] * len(batch[0]))] * len(batch))

        # 构建批量插入的占位符
        placeholders = []
        for record in batch:
            placeholders.append(sql.SQL("({})").format(sql.SQL(", ").join([sql.Placeholder()] * len(record))))
        placeholders_sql = sql.SQL(", ").join(placeholders)

        
        values = []
        for record in batch:
            values.extend(record[col] for col in batch[0].keys())

        # sql_query = """
        # INSERT INTO {schema}.{table} ({columns}) VALUES {placeholders} 
        # ON CONFLICT {conflict_target} {do_update_set};
        # """

        # 构建SQL查询
        if do_update_set==None:
            sql_query = sql.SQL("""
                INSERT INTO {schema}.{table} ({columns}) VALUES {placeholders};
            """).format(
                schema = sql.Identifier(schema),
                table = sql.Identifier(table),
                columns=columns,
                placeholders=placeholders_sql,  # 注意：这里可能需要根据实际情况调整如何插入占位符
            )
        else:
            sql_query = sql.SQL("""
                INSERT INTO {schema}.{table} ({columns}) VALUES {placeholders} 
                ON CONFLICT {conflict_target} {do_update_set};
            """).format(
                schema = sql.Identifier(schema),
                table = sql.Identifier(table),
                columns=columns,
                placeholders=placeholders_sql,  # 注意：这里可能需要根据实际情况调整如何插入占位符
                conflict_target=conflict_target,
                do_update_set=do_update_set
            )
            
        
        async with self.pool.connection() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute(sql_query, values)
                    await conn.commit()
                    logger.info(f"成功处理第 {start_index + 1} 到 {end_index} 条记录，共 {cur.rowcount} 条")
                    return cur.rowcount
            except Exception as e:
                await conn.rollback()
                logger.error(f"处理第 {start_index + 1} 到 {end_index} 条记录时发生错误: {e}")
                logger.error(f"错误行号: {e.__traceback__.tb_lineno}")
                raise

    async def upsert_data(self, schema: str, table: str, data: List[Dict[str, Any]], 
                         batch_size: int = None, update: bool = False, 
                         create: bool = False, add_columns: bool = False,
                         skipPK=False,only_column: bool = False) -> int:
        """
        异步批量插入或更新数据
        :param schema: 模式名
        :param table: 表名
        :param data: 数据列表，每个元素为一个字典，键为列名，值为列值
        :param batch_size: 每批次处理的记录数，默认为65535/列数
        :param update: 是否更新已存在的记录，默认为False
        :param create: 如果表不存在，是否创建表，默认为False
        :param add_columns: 如果列不存在，是否添加列，默认为False
        :param only_column: 是否只更新数据库中存在的列，默认为False
        :param skipPK: 是否跳过主键检查，默认为False不跳过
        :return: 处理的总记录数
        """
        
        if not isinstance(data, list) or not data:
            raise ValueError("无效的数据列表输入")

        if not await self.check_table(schema, table):
            if create:
                columns = {key: self.infer_data_type(value) 
                         for key, value in (data[0] if data else {}).items()}
                await self.create_table(schema, table, columns)
            else:
                raise ValueError(f"表 '{schema}.{table}' 不存在")

        db_columns = await self.get_columns(schema, table)  # 数据库中的列
        all_columns = set().union(*(d.keys() for d in data)) # data中所有的列
        missing_columns = all_columns.difference(db_columns) # data中有 数据库中不存在的列

        if missing_columns:
            if add_columns:
                for col in missing_columns:
                    sample_value = next((d[col] for d in data if col in d), None)
                    col_type = self.infer_data_type(sample_value)
                    await self.add_column(schema, table, col, col_type)
                    db_columns[col] = col_type
            elif only_column:
                filter_data = ({k: d[k] for k in db_columns.keys() if k in d} for d in data)
                data = list(filter_data)
            else:
                raise ValueError(f"表 '{schema}.{table}' 中缺少列: {', '.join(missing_columns)}")

        batch_size_max = int(65535/len(data[0]))
        if not batch_size or batch_size > batch_size_max:
            batch_size = batch_size_max
            logger.info(f"batch_size 最大可设置为 {batch_size}")

        if not skipPK:
            primary_keys = await self.get_primary_keys(schema, table)
            if not primary_keys:
                raise ValueError("没有找到主键,未保证数据一致性暂停写入")

            # conflict_target = '({})'.format(', '.join(primary_keys))
            # do_update_set = "DO UPDATE SET " + ', '.join(
            #     [f"{col} = EXCLUDED.{col}" for col in data[0].keys() 
            #      if col not in primary_keys]) if update else "DO NOTHING"

            # 构建 CONFLICT 目标
            conflict_target = sql.SQL('({})').format(
                sql.SQL(', ').join(map(sql.Identifier, primary_keys))
            )

            # 构建 DO UPDATE SET 子句
            if update:
                do_update_set = sql.SQL("DO UPDATE SET {updates}").format(
                    updates=sql.SQL(', ').join(
                        sql.SQL("{col} = EXCLUDED.{col}").format(
                            col=sql.Identifier(col)
                        )
                        for col in data[0].keys() if col not in primary_keys
                    )
                )
            else:
                do_update_set = sql.SQL("DO NOTHING")
        else:
            conflict_target = None
            do_update_set=None

        total_count = 0
        tasks = []
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            end_index = min(i + batch_size - 1, len(data) - 1)
            task = self.upsert_batch(schema, table, batch, conflict_target, 
                                   do_update_set, i, end_index)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"批处理失败: {result}")
                raise result
            else:
                total_count += result

        return total_count

    async def get_primary_keys(self, schema: str, table: str) -> List[str]:
        """
        获取给定表的主键列表。
        
        :param schema: 模式名
        :param table: 表名
        :return: 主键列表
        """
        query = """
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attnum = ANY(i.indkey) AND a.attrelid = i.indrelid
        WHERE  i.indrelid = %s::regclass
        AND    i.indisprimary;
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (f'"{schema}"."{table}"',))
                primary_keys = [row[0] for row in await cur.fetchall()]
                if not primary_keys:
                    logger.error(f"表 '{schema}.{table}' 没有主键")
                    raise ValueError(f"表 '{schema}.{table}' 没有主键")
                return primary_keys


