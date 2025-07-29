import collections
from ..utils.general import ddl 
from dataclasses import dataclass

@dataclass
class information_schema:
    sql_columns:str
    sql_pks:str
    sql_index:str
    sql_table_comments:str
    sql_datadict:str
    sql_table_create:str
    sql_view_create:str
    sql_function_create:str

class metedata_schema(information_schema):
    def __init__(self,*args,**kwargs):
        self.current_schema = ''
        super().__init__(**kwargs)

    def get_datadict(self,database=''):
        '''数据字典'''
        self.cursor.execute(self.sql_datadict.format(database = database if database else self.current_schema))
        data = self.cursor.fetchall()
        return data 

    def get_table_pk(self,table,database=''):
        '''获取主键字段
        Parameres
        -----------
        conn:DBAPI
            数据库连接对象
        table:str
            表名
        '''
        self.cursor.execute(self.sql_pks.format(table_name = table,database= database if database else self.current_schema ))
        cons = [n[0] for n in self.cursor.fetchall() if n[0]]
        return cons

    def get_inidex(self):
        pass

    def get_table_description(self,table,database=''):
        '''获取字段
        (字段名称、数据类型、数据长度、精度、允许为空、默认值)
        '''
        cols = collections.defaultdict(list)
        self.cursor.execute(self.sql_columns.format(table_name = table,database= database if database else self.current_schema))
        return self.cursor.fetchall()

    def get_table_create(self,table,database='',to_table=''):
        '''table ddl'''
        #self.cursor.execute(self.sql_table_create.format(table_name =table,database = database if database else self.current_schema))
        #res = self.cursor.fetchone()
        columns = self.get_table_description(table,database)
        table = to_table if to_table else table
        return ddl.table(table,columns)

    def get_table_comments(self,table,database=''):
        '''表注释
        '''
        self.cursor.execute(self.sql_table_comments.format(table_name = table,database= database if database else self.current_schema))
        res = self.cursor.fetchone()
        return res

    def get_view_create(self,table,database=''):
        '''table ddl'''
        self.cursor.execute(self.sql_view_create.format(table_name =table,database = database if database else self.current_schema))
        res = self.cursor.fetchone()
        return res
    
    def get_function_create(self,table,database=''):
        '''table ddl'''
        self.cursor.execute(self.sql_function_create.format(table_name =table,database = database if database else self.current_schema))
        res = self.cursor.fetchone()
        return res

