from sqlalchemy import create_engine, inspect
from datamation.db.utils.general import sqlalchemy_engine

class DialectAdapter:
    """数据库适配器基类"""
    
    def __init__(self, engine):
        self.engine = engine

    def type_mapping(self, column_type):
        """类型映射，子类实现"""
        return str(column_type)

    def format_column(self, column):
        """格式化列定义"""
        column_def = f"{column['name']} {self.type_mapping(column['type'])}"
        if column.get('nullable') is False:
            column_def += " NOT NULL"
        if column.get('default') is not None:
            column_def += f" DEFAULT {column['default']}"
        return column_def

    def generate_add_column_sql(self, table_name, column):
        """添加字段的 SQL"""
        return f"ALTER TABLE {table_name} ADD COLUMN {self.format_column(column)};"

    def generate_alter_column_sql(self, table_name, column):
        """修改字段的 SQL，子类可重写"""
        return f"ALTER TABLE {table_name} ALTER COLUMN {column['name']} TYPE {self.type_mapping(column['type'])};"

    def generate_table_comment_sql(self, table_name, comment):
        """表注释 SQL"""
        return f"COMMENT ON TABLE {table_name} IS '{comment}';"

    def generate_column_comment_sql(self, table_name, column_name, comment):
        """字段注释 SQL"""
        return f"COMMENT ON COLUMN {table_name}.{column_name} IS '{comment}';"


class MySQLAdapter(DialectAdapter):
    """MySQL 适配器"""

    def type_mapping(self, column_type):
        type_map = {
            "INTEGER": "INT",
            "VARCHAR": "VARCHAR",
            "TEXT": "TEXT",
            "BOOLEAN": "TINYINT(1)",
        }
        return type_map.get(str(column_type).upper(), str(column_type))

    def generate_alter_column_sql(self, table_name, column):
        """MySQL 变更字段语法"""
        return f"ALTER TABLE {table_name} MODIFY {self.format_column(column)};"


class PostgreSQLAdapter(DialectAdapter):
    """PostgreSQL 适配器"""

    def type_mapping(self, column_type):
        type_map = {
            "INT": "INTEGER",
            "VARCHAR": "TEXT",
            "TINYINT(1)": "BOOLEAN",
        }
        return type_map.get(str(column_type).upper(), str(column_type))


def get_adapter(dialect, engine):
    """获取适配器实例"""
    adapters = {
        "mysql": MySQLAdapter,
        "postgresql": PostgreSQLAdapter,
    }
    return adapters.get(dialect, DialectAdapter)(engine)


def generate_create_table_statements(insp, adapter,tables =[]):
    """生成创建表的 SQL 语句"""
    if tables:
        table_names = tables
    else:
        table_names = insp.get_table_names()

    create_statements = []

    for table_name in table_names:
        columns = insp.get_columns(table_name)
        pk_constraint = insp.get_pk_constraint(table_name)
        pk_columns = pk_constraint.get('constrained_columns', [])

        column_definitions = [adapter.format_column(col) for col in columns]
        if pk_columns:
            column_definitions.append(f"PRIMARY KEY ({', '.join(pk_columns)})")

        create_statement = f"\nCREATE TABLE {table_name} (\n" + ",\n".join(column_definitions) + "\n);\n"
        create_statements.append(create_statement)  

        table_comment = insp.get_table_comment(table_name)
        if table_comment:
            create_statements.append(adapter.generate_table_comment_sql(table_name, table_comment))

        for column in columns:
            if column.get('comment'):
                create_statements.append(adapter.generate_column_comment_sql(table_name, column['name'], column['comment']))

    return create_statements


def generate_alter_table_statements(old_insp, new_insp, adapter):
    """生成 ALTER TABLE 语句"""
    old_tables = old_insp.get_table_names()
    new_tables = new_insp.get_table_names()
    alter_statements = []

    # 处理新增表
    for table_name in (set(old_tables) - set(new_tables)):
        alter_statements.extend(generate_create_table_statements(old_insp, adapter,tables=[table_name]))

    # 处理字段变化
    for table_name in set(old_tables) & set(new_tables):
        old_columns = {col['name']: col for col in old_insp.get_columns(table_name)}
        new_columns = {col['name']: col for col in new_insp.get_columns(table_name)}

        for column_name, new_column in new_columns.items():
            if column_name not in old_columns:
                alter_statements.append(adapter.generate_add_column_sql(table_name, new_column))
            else:
                old_column = old_columns[column_name]
                if str(old_column['type']) != str(new_column['type']):
                    alter_statements.append(adapter.generate_alter_column_sql(table_name, new_column))
                if str(old_column.get('nullable')) != str(new_column.get('nullable')):
                    alter_statements.append(
                        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {'DROP' if new_column.get('nullable') else 'SET'} NOT NULL;"
                    )
                if str(old_column.get('default')) != str(new_column.get('default')):
                    alter_statements.append(
                        f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DEFAULT {new_column['default']};"
                    )
                if str(old_column.get('comment')) != str(new_column.get('comment')):
                    alter_statements.append(
                        adapter.generate_column_comment_sql(table_name, column_name, new_column['comment'])
                    )

        for column_name in set(old_columns.keys()) - set(new_columns.keys()):
            alter_statements.append(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")

    return alter_statements

def get_sqldb_diff(source_conn, target_conn, target_dialect):
    """对比两个数据库并生成 SQL

    Parameters
    ----------
    source_conn : callable
        一个可调用对象，用于创建源数据库连接。例如：lambda: raw_connection
    target_conn : callable
        一个可调用对象，用于创建目标数据库连接。例如：lambda: raw_connection
    target_dialect : str
        目前支持的数据库类型 "mysql" 或 "postgresql"
    """
    source_engine = sqlalchemy_engine(source_conn)
    target_engine = sqlalchemy_engine(target_conn)
    target_adapter = get_adapter(target_dialect, target_engine)

    old_insp = inspect(source_engine)
    new_insp = inspect(target_engine)

    return generate_alter_table_statements(old_insp, new_insp, target_adapter)

def get_sqldb_ddl(source_conn, dialect, tables=[]):
    """获取数据库的 DDL 语句"""
    engine = sqlalchemy_engine(source_conn)
    adapter = get_adapter(dialect, engine)
    insp = inspect(engine)

    return generate_create_table_statements(insp, adapter,tables)

def _genericize_column_types(inspector, tablename: str, column_dict: dict) -> None:
    """将列类型转换为通用类型"""
    column_dict["type"] = column_dict["type"].as_generic()

def sqldb_structure_sync(source_conn,target_conn,table:str)->str:
    """基于 sqlalchemy 进行跨数据库结构转换
    
    Args:
        source_conn: 源数据库连接
        target_conn: 目标数据库连接
        table: 要同步的表名
        
    Returns:
        生成的 DDL 语句，如果失败则返回空字符串
    """
    from sqlalchemy import event, MetaData, Table
    from sqlalchemy.schema import CreateTable

    metadata = MetaData()
    event.listen(metadata, "column_reflect", _genericize_column_types)

    try:
        table_obj = Table(table, metadata, autoload_with=source_conn)
        create_stmt = CreateTable(table_obj).compile(target_conn)
        return str(create_stmt)
    except Exception:
        return ''