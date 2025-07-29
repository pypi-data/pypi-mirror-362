
import sqlite3
import pickle
import datetime
import itertools

__all__=['Cache_database','kdb']

def adapt_py(obj):
    return pickle.dumps(obj)

def convert_py(obj):
    return pickle.loads(obj)

def Cache_database(table_name,columns,datetime_cols = [],mode = None,adapt=[],location = ':memory:'):
    '''本地缓存数据库 默认支持数据类型 int、float、str、bool

    Parameters
    ------------
    table_name:str
        表名称
    columns:str
        需要创建的字段名称
    datetime_col:list
        指定datetime数据类型的字段
    mode:str
        默认 None
        python 支持类型较多 目前支持python常见内置类型 
        set,list,dict,tuple,str,bool,range,int,bytes,float,complex,None,datetime.datetime

        python模式会对性能有影响 根据场景酌情使用
    adapt:list
        当mode为python时 可自定义添加类型支持 如numpy、pandas等常见数据类型
    '''
    conn = sqlite3.connect(location, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute('PRAGMA synchronous = OFF')
    cur.execute('PRAGMA journal_mode = OFF')

    if mode =='python ':
        sql_cols = [n+' py' for n in columns]
        for apt in [str,int,bytes,datetime.datetime,datetime.time,datetime.date,float,bool,set,list,dict,tuple,range,complex,None]:
            sqlite3.register_adapter(apt,adapt_py)
        for apt in  adapt:
            sqlite3.register_adapter(apt,adapt_py)
        sqlite3.register_converter('py',convert_py)
    else:
        sql_cols = [n+' timestamp ' if n in datetime_cols else n for n in columns]

    field = ','.join(sql_cols)
    create_sql = "create table {} ({})".format(table_name,field)
    cur.execute(create_sql)
    return conn

class kdb(object):
    def __init__(self,name =':memory:',adapt=[]):
        '''基于sqlite实现的字典 原生支持 number、string、bool、byte
        可对字典进行持久化
        
        Parameters
        ------------
        name:str
            :memory 默认使用内存 功能与原生字典一致 但是效率比原生字典差很多
            指定路径则使用文件系统
        adapt:list
            自定义的扩展数据类型
        '''
        for apt in [set,list,dict,tuple,str,bool,range,int,bytes,float,complex,None,datetime.datetime]:
            sqlite3.register_adapter(apt,adapt_py)

        for apt in  adapt:
            sqlite3.register_adapter(apt,adapt_py)

        sqlite3.convert_py('py',convert_py)
        self.__conn = sqlite3.connect(name,cached_statements = 1000,detect_types=sqlite3.PARSE_DECLTYPES)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('PRAGMA synchronous = OFF')
        self.__cursor.execute('PRAGMA journal_mode = OFF')
        self.__cursor.execute('CREATE TABLE kv (k,v py)')
        self.__cursor.execute('CREATE UNIQUE INDEX K_IDX on KV (K)')
        
    def __missing__(self):
        pass

    def __getitem__(self,k):
        self.__cursor.execute('select v from kv where k = :0',[k])
        v = self.__cursor.fetchone()
        if v:
            return v[0]
        else:
            raise KeyError(k)

    def __setitem__(self,k,v):
        self.__cursor.execute('replace into kv values(:0,:1)',[k,v])

    def __delitem__(self,k):
        self.__cursor.execute('delete from kv where k = :0',[k])

    def __iter__(self):
        self.__cursor.execute('select k from kv')
        for row in self.__cursor:
            yield row[0]

    def __len__(self):
        self.__cursor.execute('select count(k) from kv')
        v = self.__cursor.fetchone()[0]
        return v

    def __contains__(self,k):
        self.__cursor.execute('select count(k) from kv where k =:0',[k])
        v = self.__cursor.fetchone()[0]
        if v >0:
            return True
        else:
            return False

    def __or__(self,other):
        if issubclass(other.__class__,dict):
            new_obj = locals()
            new_obj.update(self,other)
        else:
            raise TypeError(type(other))

    def __eq__(self,other):
        for k,v in other.items():
            self.get(k,None)!= v
            return False
        return True

    def get(self,k,default =None):
        self.__cursor.execute('select v from kv where k = :0',[k])
        v = self.__cursor.fetchone()[0]
        if v:
            return v
        else:
            if default:
                return default
            else:
                raise KeyError(k)

    def clear(self):
        self.__cursor.execute('truncate table kv')

    def pop(self,k):
        v = self.__getitem__(k)
        self.__delitem__(k)
        return v

    def update(self,*arg,**kwargs):
        for other in arg:
            self.__cursor.executemany('replace into kv values(:0,:1)',list(other.items()))
        if kwargs:
            self.__cursor.executemany('replace into kv values(:0,:1)',list(kwargs.items()))

    def keys(self):
        self.__cursor.execute('select k from kv')
        return (row[0] for row in self.__cursor)
            
    def values(self):
        self.__cursor.execute('select v from kv')
        return (row[0] for row in self.__cursor)

    def setdefault(self,k,v):
        sql = 'insert into kv (k,v) select :0,:1 where not exists (select 1 from kv t where t.k=:2);'
        self.__cursor.execute(sql,[k,v,k])
        v = self.__getitem__(k)
        return v

    def fromkeys(self,iterable,default_value = None):
        '批量设置键'
        iter = itertools.zip_longest(iterable,[default_value])
        self.__cursor.executemany('replace into kv values(:0,:1)',iter)

    def iter(self):
        self.__cursor.execute('select k from kv')
        v = self.__cursor.fetchone()
        if v:
            yield v[0]

    def items(self):
        self.__cursor.execute('select k,v from kv')
        yield self.__cursor.fetchone()
        