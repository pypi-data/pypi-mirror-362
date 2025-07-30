# 这个是优化后的正式版本
import sys
import os
import logging
import time
import io
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
from psycopg import sql
import psycopg

sys.path.append(os.getcwd())
from pgmanage.syncpg.connect import PgPool

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CopyToPGSQL:
    """
    使用COPY方法将数据高效写入PostgreSQL数据库（psycopg3同步版本）
    优化点：
    1. 使用连接池管理连接
    2. 自动关闭游标和释放连接
    3. 更好的错误处理和事务管理
    4. 更精确的类型推断
    5. 内存优化，减少临时文件使用
    """

    def __init__(self):
        """
        初始化数据库连接池
        
        :param pool: PgPool连接池对象
        """
        pass

    def _get_pgsql_type_mapping(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        更精确的DataFrame到PostgreSQL类型映射
        
        :param df: 输入DataFrame
        :return: 列名到PostgreSQL类型的字典
        """
        type_mapping = {
            'integer': 'INTEGER',
            'floating': 'FLOAT',
            'boolean': 'BOOLEAN',
            'datetime': 'TIMESTAMP',
            'date': 'DATE',
            'timedelta': 'INTERVAL',
            'string': 'varchar',
            'empty': 'varchar',
            'categorical': 'varchar',
            'list': 'JSON',
            'mixed-list': 'JSON',
            'dict': 'JSON',
            'mixed': 'varchar',
            'bytes': 'BYTEA',
            'decimal': 'NUMERIC',
            'complex': 'varchar',
            'interval': 'INTERVAL',
            'path': 'varchar',
            'url': 'varchar',
            'email': 'varchar',
            'ip': 'INET',
            'uuid': 'UUID',
            'geometry': 'GEOMETRY',
        }
        
        return {
            col: type_mapping.get(str(df[col].dtype), 'TEXT')
            for col in df.columns
        }

    def _create_table(self, conn: psycopg.Connection, schema: str, table: str, 
                     columns: Dict[str, str], primary_key: Optional[str] = None) -> None:
        """
        创建数据库表
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :param columns: 列定义的字典
        :param primary_key: 可选主键列名
        """
        with conn.cursor() as cur:
            cols_sql = ', '.join([f'"{col}" {ctype}' for col, ctype in columns.items()])
            pk_sql = f', PRIMARY KEY ("{primary_key}")' if primary_key else ""
            create_sql = f'CREATE TABLE "{schema}"."{table}" ({cols_sql}{pk_sql});'
            
            cur.execute(create_sql)
            logger.info(f"创建表 '{schema}.{table}' 成功")

    def _get_db_columns_types(self, conn: psycopg.Connection, schema: str, table: str) -> Dict[str, str]:
        """
        获取数据库中表的列名和类型
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :return: 列名到类型的字典
        """
        with conn.cursor() as cur:
            query = """
                SELECT
                    a.attname AS column_name,
                    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type
                FROM pg_catalog.pg_attribute a
                JOIN pg_catalog.pg_class t ON a.attrelid = t.oid
                JOIN pg_catalog.pg_namespace s ON t.relnamespace = s.oid
                WHERE t.relname = %s AND s.nspname = %s 
                AND a.attnum > 0 AND NOT a.attisdropped
                ORDER BY a.attnum
            """
            cur.execute(query, (table, schema))
            return {row[0]: row[1] for row in cur.fetchall()}

    def _add_columns(self, conn: psycopg.Connection, schema: str, table: str, 
                    columns: Dict[str, str]) -> None:
        """
        向数据库表中添加多列
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :param columns: 列名到类型的字典
        """
        with conn.cursor() as cur:
            alter_statements = [
                f'ADD COLUMN "{col}" {ctype}'
                for col, ctype in columns.items()
            ]
            
            add_cols_sql = f'ALTER TABLE "{schema}"."{table}" {", ".join(alter_statements)};'
            cur.execute(add_cols_sql)
            
            for col in columns:
                logger.info(f"向表 '{schema}.{table}' 添加列 '{col}' 成功")

    def _get_primary_keys(self, conn: psycopg.Connection, schema: str, table: str) -> List[str]:
        """
        获取给定表的主键列表
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :return: 主键列名列表
        """
        with conn.cursor() as cur:
            query = """
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attnum = ANY(i.indkey) AND a.attrelid = i.indrelid
            JOIN pg_class t ON t.oid = i.indrelid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE n.nspname = %s AND t.relname = %s AND i.indisprimary;
            """
            cur.execute(query, (schema, table))
            return [row[0] for row in cur.fetchall()]

    def _prepare_table_structure(self, conn: psycopg.Connection, schema: str, table: str, 
                               data: pd.DataFrame, create: bool, add_columns: bool, 
                               db_only: bool) -> List[str]:
        """
        准备表结构，返回有效的列名列表
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :param data: 输入DataFrame
        :param create: 是否创建表
        :param add_columns: 是否添加列
        :param db_only: 是否只使用数据库已有列
        :return: 有效列名列表
        """
        db_columns_type = self._get_db_columns_types(conn, schema, table)
        
        # 表不存在且需要创建
        if not db_columns_type and create:
            columns = self._get_pgsql_type_mapping(data)
            self._create_table(conn, schema, table, columns)
            db_columns_type = self._get_db_columns_types(conn, schema, table)
        elif not db_columns_type:
            raise ValueError(f"表 '{schema}.{table}' 不存在且未设置create=True")
        
        db_columns = set(db_columns_type.keys())
        data_columns = set(data.columns)
        
        # 列差异分析
        missing_in_db = data_columns - db_columns
        missing_in_data = db_columns - data_columns
        
        if missing_in_db:
            logger.info(f"数据中存在但数据库{schema}.{table}中不存在的列: {missing_in_db}")
            if add_columns:
                add_columns_dict = {
                    col: self._get_pgsql_type_mapping(data[[col]])[col]
                    for col in missing_in_db
                }
                self._add_columns(conn, schema, table, add_columns_dict)
                db_columns_type.update(add_columns_dict)
                db_columns.update(missing_in_db)
            elif not db_only:
                raise ValueError(f"数据库{schema}.{table}中缺少列: {missing_in_db}")
        
        if missing_in_data:
            logger.info(f"数据库{schema}.{table}中存在但数据中不存在的列: {missing_in_data}")
        
        return [col for col in data.columns if col in db_columns]

    def _create_temp_table_and_copy(self, conn: psycopg.Connection, temp_table: str, 
                                  schema: str, table: str, data: pd.DataFrame) -> None:
        """
        创建临时表并COPY数据
        
        :param conn: 数据库连接对象
        :param temp_table: 临时表名
        :param schema: 模式名
        :param table: 目标表名
        :param data: 要导入的数据
        """
        with conn.cursor() as cur:
            db_columns_type = self._get_db_columns_types(conn, schema, table)
            columns_sql = sql.SQL(', ').join(
                sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(db_columns_type[col]))
                for col in data.columns
            )
            
            # 创建临时表
            cur.execute(sql.SQL("""
                CREATE TEMP TABLE {temp_table} (
                    {columns}
                ) ON COMMIT DROP;
            """).format(
                temp_table=sql.Identifier(temp_table),
                columns=columns_sql
            ))
            
            # 使用内存缓冲区COPY数据
            with io.StringIO() as buffer:
                data.to_csv(buffer, index=False, header=False)
                buffer.seek(0)
                
                with cur.copy(
                    sql.SQL("COPY {table} FROM STDIN WITH (FORMAT csv)").format(
                        table=sql.Identifier(temp_table)
                    )
                ) as copy:
                    copy.write(buffer.read())

    def _execute_insert_update(self, conn: psycopg.Connection, schema: str, table: str, 
                             temp_table: str, valid_headers: List[str], 
                             update: Union[bool, List[str]], skipPK: bool) -> int:
        """
        执行最终的INSERT/UPDATE操作
        
        :param conn: 数据库连接对象
        :param schema: 模式名
        :param table: 表名
        :param temp_table: 临时表名
        :param valid_headers: 有效列名列表
        :param update: 更新模式
        :param skipPK: 是否跳过主键检查
        :return: 影响的行数
        """
        with conn.cursor() as cur:
            primary_keys = self._get_primary_keys(conn, schema, table)
            if not primary_keys:
                logger.warning(f"表 '{schema}.{table}' 没有主键")
                if not skipPK:
                    raise ValueError(f"表 '{schema}.{table}' 没有主键不允许写入,请设置主键或者设置skipPK=True忽略主键检查")
            
            # 构建基础SQL
            full_table = sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))
            insert_cols = sql.SQL(', ').join(sql.Identifier(c) for c in valid_headers)
            
            insert_sql = sql.SQL("""
                INSERT INTO {target_table} ({insert_cols})
                SELECT {select_cols} FROM {temp_table}
            """).format(
                target_table=full_table,
                insert_cols=insert_cols,
                select_cols=insert_cols,
                temp_table=sql.Identifier(temp_table),
            )
            
            # 处理冲突
            if primary_keys:  # 确保有主键时才添加ON CONFLICT子句
                pk_cols = sql.SQL(', ').join(sql.Identifier(c) for c in primary_keys)
                
                if update is False:
                    insert_sql += sql.SQL(" ON CONFLICT ({pk_cols}) DO NOTHING").format(
                        pk_cols=pk_cols
                    )
                elif update is True:
                    update_cols = [c for c in valid_headers if c not in primary_keys]
                    if update_cols:
                        insert_sql += sql.SQL("""
                            ON CONFLICT ({pk_cols}) DO UPDATE SET
                                {update_cols}
                        """).format(
                            pk_cols=pk_cols,
                            update_cols=sql.SQL(', ').join(
                                sql.SQL("{col} = EXCLUDED.{col}").format(col=sql.Identifier(c))
                                for c in update_cols
                            )
                        )
                    else:
                        # 如果没有可更新的列，则退化为DO NOTHING
                        insert_sql += sql.SQL(" ON CONFLICT ({pk_cols}) DO NOTHING").format(
                            pk_cols=pk_cols
                        )
                elif isinstance(update, list):
                    update_cols = [c for c in update if c in valid_headers and c not in primary_keys]
                    if update_cols:
                        insert_sql += sql.SQL("""
                            ON CONFLICT ({pk_cols}) DO UPDATE SET
                                {update_cols}
                        """).format(
                            pk_cols=pk_cols,
                            update_cols=sql.SQL(', ').join(
                                sql.SQL("{col} = EXCLUDED.{col}").format(col=sql.Identifier(c))
                                for c in update_cols
                            )
                        )
                    else:
                        # 如果没有有效的更新列，则退化为DO NOTHING
                        insert_sql += sql.SQL(" ON CONFLICT ({pk_cols}) DO NOTHING").format(
                            pk_cols=pk_cols
                        )
                else:
                    raise ValueError("update参数必须为bool或list类型")
            
            cur.execute(insert_sql)
            return cur.rowcount

    def copyrun(self,conn, schema: str, table: str, data: pd.DataFrame,
               update: Union[bool, List[str]] = False, create: bool = False,
               add_columns: bool = False, db_only: bool = False, skipPK: bool = False) -> int:
        """
        将数据使用COPY方法高效写入PostgreSQL
        :param conn: 数据库连接池
        :param schema: 模式名
        :param table: 表名
        :param data: 要写入的数据
        :param update: 更新模式(False:不更新, True:更新所有, List:更新指定列)
        :param create: 表不存在时是否创建
        :param add_columns: 是否自动添加缺失列
        :param db_only: 是否只写入数据库中存在的列
        :param skipPK: 是否跳过主键检查,默认为False不跳过
        :return: 影响的行数
        """
        start_time = time.time()
        
        # 从连接池获取连接
   
        try:
            with conn.transaction():
                # 1. 准备表结构
                valid_headers = self._prepare_table_structure(
                    conn, schema, table, data, create, add_columns, db_only
                )
                
                # 2. 创建临时表并COPY数据
                temp_table = "temp_import_table"
                self._create_temp_table_and_copy(
                    conn, temp_table, schema, table, data[valid_headers]
                )
                
                # 3. 执行插入/更新
                result_count = self._execute_insert_update(
                    conn, schema, table, temp_table, valid_headers, update, skipPK
                )
                
                logger.info(
                    f"✅ 数据写入完成，耗时：{time.time() - start_time:.2f}秒, "
                    f"写入行数：{result_count}"
                )
                return result_count
                
        except Exception as e:
            conn.rollback()
            logger.error(f"数据写入失败: {str(e)}")
            raise


if __name__ == '__main__':
    # 示例用法
    import pandas as pd
    from pdcleaner import DataSet

    # 初始化连接池
    PGLINK_URL = 'dbname=shop_data host=127.0.0.1 port=5432 user=postgres password=manji1688'
    conn=psycopg.connect(PGLINK_URL)

    
    # 示例数据
    schema = 'douyin_shop'
    table = 'dy_dp_dd_ddgl_bzbb_copy12'
    data = pd.read_csv(r"C:\Users\manji\Downloads\抖音订单\1752550967_6e03f011910e5e4414e47f8f6dc317c8OtkVGLHs.csv", dtype=str)
    data = DataSet.clean_data(data, add_time=True)
    print(f"数据清洗完成，数据行数: {len(data)}")


    # 执行COPY
    copier = CopyToPGSQL()
    copier.copyrun(
        conn=conn,
        schema=schema,
        table=table,
        data=data,
        update=True,
        create=True,
        db_only=True,
        skipPK=True
    )

    conn.close()
