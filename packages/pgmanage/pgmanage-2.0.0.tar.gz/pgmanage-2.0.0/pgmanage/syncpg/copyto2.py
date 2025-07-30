# 这个是原始版本（测试使用，并没有使用）
import sys,os
sys.path.append(os.getcwd())

import logging
import time
import os
import tempfile
from typing import Dict, List, Any, Optional,Union
import asyncio
import pandas as pd


from pgmanage.asyncpg.connect import AsyncPgPool
from pdcleaner import DataSet

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




# 使用copy方法讲数据写入到PostgreSQL数据库
class CopyToPGSQL():
    """
    使用copy方法将数据写入到PostgreSQL数据库
    
    """

    def __init__(self,conn, cur: str = None):
        """
        初始化数据库连接配置。
        
        :param conn_str: 数据库连接字符串
        """
        self.conn = conn
        self.cur = cur

    # 检查表是否存在
    def _check_table(self, schema: str, table: str) -> bool:
        """
        检查表是否存在。
        
        :param schema: 模式名
        :param table: 表名
        :return: 如果存在返回True，否则False
        """
        querystr = f"""
        SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table}');
        """
        self.cur.execute(querystr)
        exists = cur.fetchone()[0]
        return exists

    # 根据df获取pgsql数据类型映射关系
    def _get_pgsql_type_mapping(self, df: pd.DataFrame):
        """
        根据df获取pgsql数据类型映射关系
        :return: 数据类型映射关系
        """
        def infer_pgsql_type(col):
            # 使用 pandas 的内部类型推断
            inferred_type = pd.api.types.infer_dtype(col, skipna=True)

            # 更全面的类型映射
            type_mapping = {
                'integer': 'INTEGER',
                'floating': 'FLOAT',
                'boolean': 'BOOLEAN',
                'datetime': 'TIMESTAMP',
                'date': 'DATE',
                'timedelta': 'INTERVAL',
                'string': 'TEXT',
                'empty': 'TEXT',
                'categorical': 'TEXT',
                'list': 'JSON',
                'mixed-list': 'JSON',
                'dict': 'JSON',
                'mixed': 'TEXT',
                'bytes': 'BYTEA',
                'decimal': 'NUMERIC',
                'complex': 'TEXT',
                'interval': 'INTERVAL',
                'path': 'TEXT',
                'url': 'TEXT',
                'email': 'TEXT',
                'ip': 'INET',
                'uuid': 'UUID',
                'geometry': 'GEOMETRY',
            }

            return type_mapping.get(inferred_type, 'TEXT')
        return {col: infer_pgsql_type(df[col]) for col in df.columns}
    # 创建数据库表
    def _create_table(self, schema: str, table: str, columns: Dict[str, str], primary_key: Optional[str] = None) -> None:
        """
        创建数据库表
            :param schema: 模式名
            :param table: 表名
            :param columns: 列定义的字典，键为列名，值为列类型
            :param primary_key: 主键列名，默认为None
        """
        cols_sql = ', '.join([f'"{col}" {ctype}' for col, ctype in columns.items()])
        pk_sql = f', PRIMARY KEY ("{primary_key}")' if primary_key else ""
        create_sql = f'CREATE TABLE "{schema}"."{table}" ({cols_sql}{pk_sql});'

        self.cur.execute(create_sql)
        self.conn.commit()
        logger.info(f"创建表 '{schema}.{table}' 成功")

    # 获取数据库中表的列名和类型
    def _get_db_columns_types(self,schema:str,table:str):
        """
        获取数据库中表的列名和类型
        """
        querystr = f"""
            SELECT
                a.attname AS column_name,
                format_type(a.atttypid, a.atttypmod) AS data_type
            FROM pg_attribute a
            JOIN pg_class t ON a.attrelid = t.oid
            JOIN pg_namespace s ON t.relnamespace = s.oid
            WHERE t.relname = '{table}' AND s.nspname ='{schema}' AND a.attnum > 0 AND NOT a.attisdropped
            ORDER BY a.attnum
        """

        self.cur.execute(querystr)
        result = self.cur.fetchall()

        # 把元组组合成字典
        target_col_types = {row[0]: row[1] for row in result}
        target_columns = list(target_col_types.keys())
        logger.debug(f"📊 目标表字段及其类型: {target_col_types}")
        return target_col_types
    
    # 向数据库表中添加列。
    def _add_columns(self, schema: str, table: str, columns: dict) -> None:
        """
        向数据库表中添加多列
            :param schema: 模式名
            :param table: 表名
            :param columns: 字典，键是新列名，值是新列的数据类型
        """
        # 初始化一个列表来存储所有的ALTER TABLE语句
        alter_table_statements = []

        # 遍历传入的columns字典，为每一列构建ALTER TABLE语句
        for column, column_type in columns.items():
            alter_table_statement = f'ADD COLUMN "{column}" {column_type}'
            alter_table_statements.append(alter_table_statement)

        # 将所有单独的ALTER TABLE语句用逗号连接起来，并附加到ALTER TABLE命令上
        add_cols_sql = f'ALTER TABLE "{schema}"."{table}" {", ".join(alter_table_statements)};'
        
        # 执行SQL语句并提交更改
        self.cur.execute(add_cols_sql)
        self.conn.commit()

        # 记录信息
        for column, column_type in columns.items():
            logger.info(f"向表 '{schema}.{table}' 添加列 '{column}', 类型 '{column_type}' 成功")

    # 获取给定表的主键列表
    def _get_primary_keys(self, schema: str, table: str) -> List[str]:
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
        self.cur.execute(query, (f"{schema}.{table}",))
        primary_keys = [row[0] for row in cur.fetchall()]
        if not primary_keys:
            raise ValueError(f"表 '{schema}.{table}' 没有主键")
        return primary_keys

    def copyrun(self,
        schema: str, 
        table: str, 
        data: pd.DataFrame, 
        update: Union[bool, List[str]] = False,
        create: bool = False, 
        add_columns: bool = False,
        db_only:bool=False
        ) -> int:
        """
        将数据使用copy方法写入pgsql数据库
            :param schema: 数据库模式
            :param table: 数据库表名
            :param data: 数据
            :param update: 是否更新数据 bool or list
            :param create: 是否创建表
            :param add_columns: 是否添加列
            :param db_only: 是否只写入数据库中存在的列
        """
        start_time = time.time()

        file_headers = list(data.columns)
        db_columns_type = self._get_db_columns_types(schema, table)

        # 创建数据库表
        if not db_columns_type:
            if create:
                columns =  self._get_pgsql_type_mapping(data)
                self._create_table(schema, table,columns)
                db_columns_type = self._get_db_columns_types(schema, table)
            else:
                raise Exception(f"⚠️ 数据库表{schema}.{table} 不存在，请先创建表")

        db_columns = db_columns_type.keys()

        # 打印不一致列
        missing_in_db = list(set(file_headers) - set(db_columns))
        if missing_in_db:
            logger.info(f"⚠️ 文件中存在但数据库{schema}.{table}中不存在的列: {missing_in_db}")
        missing_in_file = list(set(db_columns) - set(file_headers))
        if missing_in_file:
            logger.info(f"⚠️ 数据库{schema}.{table}中存在但文件不存在的列: {missing_in_file}")

        # 新增数据库列
        if add_columns and missing_in_db:
            addcolumns = self._get_pgsql_type_mapping(data[[missing_in_file]])
            self._add_columns(schema, table, addcolumns)

            # 重新获取列
            db_columns_type = self.get_db_columns(schema, table)
            db_columns = db_columns_type.keys()

        # 判断是否仅写入数据库中存在的列
        if not add_columns and not db_only and  missing_in_db:
            raise Exception(f"数据库{schema}.{table}中不存在列: {missing_in_db}")

        # Step 3: 筛选 CSV 中只保留目标表中存在的列
        valid_headers = [col for col in file_headers if col in db_columns]

        # 保存临时文件用于 COPY
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv', newline='', encoding='utf-8') as tmpfile:
            data[valid_headers].to_csv(tmpfile, index=False, header=True)
            tmpfile_path = tmpfile.name

        # Step 5: 创建临时表
        temp_table = "temp_import_table"
        columns_sql = sql.SQL(', ').join(
            sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(db_columns_type[col]))
            for col in valid_headers
        )
        self.cur.execute(sql.SQL("""
            CREATE TEMP TABLE {temp_table} (
                {columns}
            ) ON COMMIT DROP;
        """).format(temp_table=sql.Identifier(temp_table), columns=columns_sql))

        # COPY 数据
        with open(tmpfile_path, 'r', encoding='utf-8') as f:
            with self.cur.copy(
                sql.SQL("COPY {table} ({cols}) FROM STDIN WITH (FORMAT csv, HEADER true)").format(
                    table=sql.Identifier(temp_table),
                    cols=sql.SQL(', ').join(sql.Identifier(c) for c in valid_headers)
                )
            ) as copy:
                copy.write(f.read())
                # self.conn.commit()

                # 执行 COPY 后检查是否有错误
                error_message = self.conn.info.error_message
                if error_message:  # 如果有错误消息
                    raise ValueError(error_message)
                
                # 使用连接状态检查（替代notices）
                if self.conn.info.transaction_status != 0:  # 0 = idle
                    logger.info(f"✅ 数据库copy事务成功，耗时：{time.time() - start_time:.2f}秒")


        os.remove(tmpfile_path)   

        # 获取主键
        primary_keys = self._get_primary_keys(schema, table)
        if not primary_keys:
            raise ValueError(f"❌ 数据库表{schema}.{table} 没有主键")
        
        # Step 8: 构建 INSERT 语句，确保列顺序与目标表完全一致
        insert_cols = [col for col in db_columns if col in valid_headers]
        select_cols = insert_cols
        full_table_name = sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))
        # 构建 INSERT 语句
        insert_sql = sql.SQL("""
            INSERT INTO {target_table} ({insert_cols})
            SELECT {select_cols} FROM {temp_table}
        """).format(
            target_table=full_table_name,
            insert_cols=sql.SQL(', ').join(sql.Identifier(c) for c in insert_cols),
            select_cols=sql.SQL(', ').join(sql.Identifier(c) for c in select_cols),
            temp_table=sql.Identifier(temp_table),
        )

        # 如果需要处理主键冲突
        if update is False:
            insert_sql += sql.SQL(" ON CONFLICT ({pk_cols}) DO NOTHING").format(
                pk_cols=sql.SQL(', ').join(sql.Identifier(c) for c in primary_keys)
            )

        elif update is True:
            # 更新所有非主键列
            update_cols = [c for c in insert_cols if c not in primary_keys]
            insert_sql += sql.SQL("""
                ON CONFLICT ({pk_cols}) DO UPDATE SET
                    {update_cols}
            """).format(
                pk_cols=sql.SQL(', ').join(sql.Identifier(c) for c in primary_keys),
                update_cols=sql.SQL(', ').join(
                    sql.SQL("{col} = EXCLUDED.{col}").format(col=sql.Identifier(c))
                    for c in update_cols
                )
            )
        elif isinstance(update, list):
            # 只更新指定列
            update_cols = [c for c in update if c in insert_cols and c not in primary_keys]
            if not update_cols:
                raise ValueError("❌ update 为列表时，必须包含非主键的可更新列")

            insert_sql += sql.SQL("""
                ON CONFLICT ({pk_cols}) DO UPDATE SET
                    {update_cols}
            """).format(
                pk_cols=sql.SQL(', ').join(sql.Identifier(c) for c in primary_keys),
                update_cols=sql.SQL(', ').join(
                    sql.SQL("{col} = EXCLUDED.{col}").format(col=sql.Identifier(c))
                    for c in update_cols
                )
            )
        else:
            raise ValueError("❌ update 参数必须为 bool 或 list 类型")
        
        self.cur.execute(insert_sql)
        self.conn.commit()
        result_count = self.cur.rowcount

        end_time = time.time() 
        logger.info(f"✅ 数据写入完成，耗时：{end_time - start_time:.2f}秒, 写入行数：{result_count}")


if __name__ == '__main__':
    import psycopg
    from psycopg import sql
    # from psycopg import sql, extensions

    PGLINK_URL = 'dbname =shop_data host = 127.0.0.1 port = 5432 user = postgres password = manji1688'
    conn = psycopg.connect(PGLINK_URL)
    cur = conn.cursor()
    
    schema = 'douyin_shop'
    table = 'dy_dp_dd_ddgl_bzbb_copy12'
    data = pd.read_csv(r"C:\Users\manji\Downloads\抖音订单\1752550967_6e03f011910e5e4414e47f8f6dc317c8OtkVGLHs.csv", dtype=str)
    data = DataSet.clean_data(data,add_time=True)
    print(f"数据清洗完成，数据行数: {len(data)}")
    
    obj =  CopyToPGSQL(conn,cur)
    # obj._get_db_columns_types(table,schema)
    # obj._check_table(schema,table)
    obj.copyrun(schema,table,data,update=True,create=True,db_only=True)

    cur.close()
    conn.close()