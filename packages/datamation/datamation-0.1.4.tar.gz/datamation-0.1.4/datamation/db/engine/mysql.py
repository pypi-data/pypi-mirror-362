
from .schema import metedata_schema

sql_columns = '''
             SELECT
                a.COLUMN_NAME as COLUMN_NAME,
                CONVERT(a.data_type,CHAR) as DATA_TYPE,
                if(a.CHARACTER_MAXIMUM_LENGTH,a.CHARACTER_MAXIMUM_LENGTH,a.NUMERIC_PRECISION) as DATA_LENGTH,
                a.NUMERIC_SCALE as DATA_SCALE,
                a.COLUMN_DEFAULT as DATA_DEFAULT,
                a.IS_NULLABLE as NULLABLE,
                CONVERT(a.COLUMN_COMMENT,CHAR) as COLUMN_COMMENT
            FROM information_schema.COLUMNS a
            where table_name = '{table_name}'
            and TABLE_SCHEMA = '{database}'
            order by TABLE_NAME,ORDINAL_POSITION
        '''
sql_pks ='''
SELECT
column_Name
FROM
INFORMATION_SCHEMA.`KEY_COLUMN_USAGE` cu
WHERE
CONSTRAINT_NAME = 'PRIMARY' AND CONSTRAINT_SCHEMA = '{database}' AND upper(cu.table_name) = '{table_name}.upper()'

'''
sql_index = '''

'''
sql_table_comments = '''
select TABLE_NAME,
    TABLE_COMMENT
from information_schema.TABLES
where TABLE_TYPE = 'BASE TABLE'
and TABLE_NAME = '{table_name}'
and TABLE_SCHEMA = '{database}'
'''

sql_datadict='''
SELECT
    a.table_schema,
    a.table_name,
    a.COLUMN_NAME as COLUMN_NAME,
    CONVERT(a.data_type,CHAR) as DATA_TYPE,
    if(a.CHARACTER_MAXIMUM_LENGTH,a.CHARACTER_MAXIMUM_LENGTH,a.NUMERIC_PRECISION) as DATA_LENGTH,
    a.NUMERIC_SCALE as DATA_SCALE,
    a.IS_NULLABLE as NULLABLE,
    a.COLUMN_DEFAULT as DATA_DEFAULT,
    CONVERT(a.COLUMN_COMMENT,CHAR) as COLUMN_COMMENT
FROM information_schema.COLUMNS a
where TABLE_SCHEMA = '{database}'
order by TABLE_NAME,ORDINAL_POSITION
'''

sql_table_create = '''
SHOW CREATE TABLE {database}.{table_name}
'''
sql_view_create = ''' 
show create view {database}.{table_name}
'''
sql_function_create = ''' 
show create function {database}.{table_name}
'''

class mysql_utility(metedata_schema):
    def __init__(self,conn):
        super().__init__(sql_columns = sql_columns,
                         sql_pks=sql_pks,sql_index = sql_index,
                         sql_table_comments=sql_table_comments,
                         sql_datadict=sql_datadict,
                         sql_table_create=sql_table_create,
                         sql_view_create=sql_view_create,
                         sql_function_create=sql_function_create)
        self.conn=conn
        self.cursor = conn.cursor()
        self.cursor.execute('select database()')
        self.current_schema = self.cursor.fetchone()[0]

    