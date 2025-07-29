
import sys

from .cache import Cache_database
from .table import table_basic
from .source import source_sql,source_pandas

__all__= ['transform_sql','pandas_sql']

sql_oracle_cons = '''
select t.TABLE_NAME,
       t.COLUMN_NAME,
       t1.CONSTRAINT_TYPE,
       t1.R_OWNER,
       R_CONSTRAINT_NAME
from user_cons_columns t left join user_constraints t1 on t.CONSTRAINT_NAME = t1.CONSTRAINT_NAME and t.TABLE_NAME = t1.table_name
'''

sql_oracle_index = '''
select a.uniqueness cons,
       b.index_name index_name,
       a.table_name table_name,
       b.column_name columns,
       dbms_metadata.get_ddl('INDEX',b.index_name) ddl_sql
from user_indexes a ,user_ind_columns b
where a.table_name=b.table_name and a.index_name = b.index_name AND a.uniqueness = 'NONUNIQUE'
'''

class transform_sql(object):
    def __init__(self,src,table_name,columns,datetime = []):
        '''将数据源转换为可使用sql查询的数据
        '''
        self._src = src
        self.columns = columns
        self.table_name
        self.cache_conn = Cache_database(table_name = self.table_name,columns = self.columns,datetime = datetime)
        self.tag = table_basic(self.cache_conn,self.table_name,columns = self.columns)
        print(self.tag.sql_insert)
        for row in self._src:
            for k,v in row.items():
                if isinstance(v,self._pandas._libs.tslibs.timestamps.Timestamp):
                    row [k] = v.to_pydatetime()
            self.tag.insert(row)
        #self.tag.endload()

def _adapt_pdate(datetime64):
    return datetime64.to_pydatetime()

class pandas_sql(transform_sql):
    def __init__(self,DataFrame,table_name):
        
        if 'pandas' in sys.modules:
            self._pandas = sys.modules['pandas']
        else:
            import pandas as pd
            self._pandas = pd

        self.df = DataFrame
        self.df = self.df.replace({self._pandas.NaT,None})
        self.df =self.df.where(self.df.notnull(), None)
        self.columns = self.df.columns.to_list()
        self.table_name = table_name
        self._src = source_pandas(self.df)
        super().__init__(self._src,table_name,self.columns)

    def execute(self,sql):
        self.cache_conn.execute(sql)
        return self.transform()

    def commit(self):
        self.cache_conn.commit()
        return self.transform()

    def transform(self):
        src= source_sql(self.cache_conn,'select * from '+ self._table_name)
        return self._pandas.DataFrame([row for row in src],columns = src.cols)





