
from pathlib import Path
import concurrent
from subprocess import call,run
import datetime
import sys 
import inspect 
import difflib
import collections 
from collections import defaultdict,Counter
from configparser import ConfigParser
import os 

__all__ = ['get_sql','inference_dtype','ddl','pep249_paramstyle','pep249_paramstyle_format',
           'get_sqltab_diff','get_sqltab_columns_diff','dbcfg']

class ddl(object):
    def pk(table_name,name,columns):
        pk = "ALTER TABLE {table_name} ADD CONSTRAINT {name} PRIMARY KEY ({columns})"
        return pk.format(table_name,name,columns)
    
    def fk(table_name,name,column,f_table_name,f_columns):
        fk = "ALTER TABLE {table_name} ADD CONSTRAINT {name} FOREIGN KEY ({columns}) REFERENCES {f_table_name}({f_columns})"
        return fk.format(table_name,name,column,f_table_name,f_columns)
    
    def unique(table_name,name,columns):
        unique = "ALTER TABLE {table_name} ADD CONSTRAINT {name} UNIQUE ({columns})"
        return unique.format(table_name=table_name,name=name,columns=columns)

    def index(table_name,columns,name = None):
        index = "CREATE INDEX {name} on {table_name} ({columns})"
        return index.format(table_name,columns,name)
    
    def table(table_name,columns,constraint = True,upper = True):
        ''' 基于数据字典生成ddl语句
        table_name:str
        columns:list
            [(字段名称,数据类型,数据长度,数据精度,默认值,可空)]
        '''
        table = 'CREATE TABLE {table_name} (\n{columns}\n)'
        field = []
        s = ''
        upper = lambda x:x.upper() if upper else lambda x:x.lower()
        for n in columns:
            s += upper(str(n[0]))+' '
            s += upper(str(n[1]))+' '
            if n[2]:
                length = str(n[2])
                if n[3]:
                    s +='('+','.join([length,str(n[3])]) + ')'
                else:
                    s +='(' + length +')'
            if len(n)>=4:
                if n[4]:
                    s += upper(' DEFAULT ')+str(n[4])+' '
            if len(n)>=5:
                if str(n[5]).upper() == 'NO':
                    s += upper(' NOT NULL ')
            field.append(s)
            s = ''
        cols_str = ',\n'.join(field)
        return table.format(table_name = table_name,columns = cols_str)

def get_sql(file):
    '''读取sql

    Parameters
    -----------
    file ：str
        path 文件的绝对路径
    Returns
    --------
    str
        返回sql字符串
    '''
    sql_str = Path(file).read_text()
    return sql_str

class dbcfg:
    ''' 读取数据库配置
    '''
    def __init__(self,file='.db'):
        ''' 读取配置

        Parameters
        ----------
        file : str, optional
            _description_, by default '.db'
        '''
        config = ConfigParser()
        # 获取当前用户目录
        user_home = os.path.expanduser('~')
        config.read(Path(user_home)/file)
        cfg = {}
        for n in config.sections():
            cfg[n] =  dict(config.items(n))
            self.__setattr__(n,cfg[n])
        self.cfg= cfg

    def keys(self):
        return list(self.cfg.keys())
    
    def __getitem__(self,index):
        return self.cfg[index]
    
    def __len__(self):
        return len(self.cfg)
    
    def __contains__(self, key):
        return key in self.cfg
    
    def __repr__(self) -> str:
        return str(self.cfg)
    
class inference_dtype(object):
    def __init__(self,d,line_num=10000):
        '''数据类型推断
           str > str
           int、float>number
           bytes > bytes
        '''
        self.d = d
        self.line_num = line_num
        self.datetime = set()
        self.number = set()
        self.str = set()
        self.field_all = set()
        self.data = []
        self.get_dtype()
        
    def get_dtype(self):
        d = self.d
        line_num = self.line_num
        num = 0
        for row in d:
            self.data.append(row)
            for k,v in row.items():
                if k not in self.field_all:
                    if isinstance(v,datetime.datetime):
                        self.datetime.add(k)
                        self.field_all.add(k)

                    elif isinstance(v,str):
                        self.str.add(k)
                        self.field_all.add(k)
                    elif isinstance(v,(int,float)):
                        self.field_all.add(k)
                        self.field_all.add(k)
                    elif isinstance(v,bytes):
                        self.bytes.add(k)
                        self.field_all.add(k)

                else:
                    return
            num+=1
            if num >=line_num:
                return

    def __iter__(self):
        for row in self.data:
            yield row

def get_sqldata_diff_pk(src_conn,src_table,target_conn,primary_key):
    '''比较两个数据库表数据差异

    Parameters
    --------------
    src_conn:dbapi
        数据库连接
    src_table:str
        表名
    target_conn:dbapi
        对比目标数据库连接
    primary_key:str
        主键
    Returns
    ---------
    dict
        {src_table:int,tag_table:int,status:bool,diff_num:int}
    '''
    src_cur = src_conn.cursor()
    tag_cur = target_conn.cursor()
    src_cur.execute(f'select {primary_key} from {src_table}')
    tag_cur.execute(f'select {primary_key} from {src_table}')
    src_pk = set(row[0] for row in src_cur)
    tag_pk = set(row[0] for row in tag_cur)
    src_cur.close()
    tag_cur.close()
    # 在src_pk中不在tag_pk中
    src_to_tag = src_pk.difference(tag_pk)
    # 在tag_pk中不在src_pk中
    tag_to_src = tag_pk.difference(src_pk)
    res = {'src_table':src_table,
            'tag_table':src_table,
            'status':src_to_tag==tag_to_src,
            'src_to_tag_diffnum':len(src_to_tag),
            'tag_to_src_diffnum':len(tag_to_src),
            'src_to_tag':src_to_tag,
            'tag_to_src':tag_to_src
            }
    return res
    
def get_sqltab_diff(src_datadict,tag_datadict):
    src_tables = list(set(table[1] for table in src_datadict))
    tag_tables = list(set(table[1] for table in tag_datadict))
    src_tables.sort()
    tag_tables.sort()
    s = difflib.SequenceMatcher(a=src_tables,b= tag_tables)
    res = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag!='equal':
            res.append((tag,src_tables[i1:i2], tag_tables[j1:j2]))
    return res

def get_sqltab_columns_diff(src_datadict,tag_datadict):
    src_cols = collections.defaultdict(list)
    for d in src_datadict:
        src_cols[d[1]].append(d[2])

    tag_cols = collections.defaultdict(list)
    for d in tag_datadict:
        tag_cols[d[1]].append(d[2])

    diff_change = []
    for table in src_cols:
        src_col = src_cols[table]
        if table in tag_cols:
            tag_col = tag_cols[table]
            src_col.sort()
            tag_col.sort()

            s = difflib.SequenceMatcher(a=src_col,b= tag_col)
            diff_res = []
            for tag, i1, i2, j1, j2 in s.get_opcodes():
                if tag!='equal':
                    diff_res.append((table,tag,src_col[i1:i2], tag_col[j1:j2]))
            if diff_res:
                diff_change.append(diff_res)
    return diff_change

def pep249_paramstyle_format(seq:list,style:str ='numeric',numeric_start:int=0):
    '''pep249 
    String constant stating the type of parameter marker formatting expected by the interface. Possible values are
    
    | paramstyle   | Meaning  |
    |  ----    | ----  |
    | qmark    | Question mark style, e.g. ...WHERE name=? |
    | numeric  | Numeric, positional style, e.g. ...WHERE name=:1 |
    | named    | Named style, e.g. ...WHERE name=:name|
    | format   | ANSI C printf format codes, e.g. ...WHERE name=%s|
    | pyformat | Python extended format codes, e.g. ...WHERE name=%(name)s|

    Parameters
    ----------
    seq : list
        序列
    style : str, optional
        使用格式, by default 'numeric'
    numeric_start : int, optional
        numeric格式时的起始编号, by default 0

    Returns
    -------
    list
        格式化后的序列
    '''
    if style == 'qmark':
        seq_ = ['?' for n in seq]
    elif style == 'numeric':
        seq_ = [':'+str(n+numeric_start) for n,v in enumerate(seq)]
    elif style == 'named':
        seq_ = [':'+n for n in seq]
    elif style == 'format':
        seq_ = ['%s' for n in seq]
    elif style == 'pyformat':
        seq_ = ['%('+n+')s' for n in seq]
    else:
        raise ValueError(style)
    return seq_

def pep249_paramstyle(conn):
    '''获取dbapi驱动所使用的绑定参数格式'''
    cursor = conn.cursor()
    api = sys.modules[inspect.getmodule(cursor).__package__]
    cursor.close()
    return api.paramstyle

def get_dialect_name(conn):
    '''判断数据库类型

    Parameters
    ----------
    conn : dbapi2.Connection
        符合pep249规范的数据库连接对象
    '''
    dialect_mapping = {
        'pymysql': 'mysql+pymysql',
        'mysql':'mysql+mysqlconnector',
        'mysqldb':'mysql+mysqldb',
        'psycopg2': 'postgresql+psycopg2',
        'psycopg':'postgresql+psycopg',
        'oracle': 'oracle+cx_oracle',
        'pymssql':'mssql+pymssql',
        'sqlite3': 'sqlite'
    }
    try:
        module_name = ''
        if inspect.getmodule(conn):
            module_path = Path(inspect.getmodule(conn).__file__)
            for index,name in enumerate(module_path.parts):
                if name.lower() in dialect_mapping:
                    module_name = name.lower()
                    break
        else:
            module_path = Path(inspect.getmodule(conn.__class__).__file__)
            for index,name in enumerate(module_path.parts):
                if name == 'site-packages':
                    module_name = module_path.parts[index+1:][0]
                    break

    except AttributeError:
        module_name = 'sqlite'

    for dialect, module in dialect_mapping.items():
        if dialect == module_name.lower():
            return module
    raise ValueError('不支持的数据库类型')

def sqlalchemy_engine(connecton):
    '''数据库连接对象转为 sqlalchemy

    Parameters
    ----------
    connecton : dbapi2.Connection,function object returning a dbapi2.Connection
    Returns
    -------
    sqlalchemy.engine
    '''
    from sqlalchemy import create_engine

    # 如果 source_db 和 target_db 不是函数对象，则将其转换为函数对象
    if  hasattr(connecton, '__call__'):
        conn = connecton()
        source_dialect_name = get_dialect_name(conn)
        conn.close()
        source_db = connecton
    else:
        source_dialect_name = get_dialect_name(connecton)
        source_db = lambda : connecton
    
    # 创建数据库引擎
    engine = create_engine(f'{source_dialect_name}://',creator=source_db)
    return engine

