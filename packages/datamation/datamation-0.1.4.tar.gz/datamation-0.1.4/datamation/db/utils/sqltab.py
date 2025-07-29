
import functools
from inspect import isfunction
from .general import sqlalchemy_engine

__all__ = ['get_sqltab_max',
           'get_sqltab_min',
           'get_sqltab_sum',
           'get_sqltab_avg',
           'get_sqltab_count',
           'get_sqltabs_count',
           'get_sqltab_cols',
           'get_sqltab_values',
           'sql_execute',
           'get_sqltab_description',
           'get_sqltab_names',
           'get_sqltab_count_diff']

def db_wrapper(func):
    def wrapper(conn_or_func, *args, **kwargs):
        if callable(conn_or_func):
            # 如果传入的是函数，则调用函数以获取数据库连接
            conn = conn_or_func()
            close_conn = True  # 需要在函数执行完毕后关闭连接
        else:
            # 如果传入的是数据库连接，则直接使用它
            conn = conn_or_func
            close_conn = False  # 不需要关闭连接
        try:
            result = func(conn, *args, **kwargs)
        except Exception as e:
            raise e
        finally:
            if close_conn:
                conn.close()
        return result
    return wrapper

def aggregate_func(func,conn,table,field):
    '''_summary_
    Parameters
    ----------
    func : dbms aggregate 
        str
    conn : dbapi pep249
        数据库连接
    field : str
        字段
    table : str
        表或者查询sql

    Returns
    -------
    _type_
        _description_
    '''
    if 'select' in table.lower():
        sql = f'select {func}({field}) d from ({table}) as tb'
    else :
        sql = f'select {func}({field}) d from {table}'
    cur = conn.cursor()
    cur.execute(sql)
    max_date = cur.fetchone()[0]
    cur.close()
    return max_date

get_sqltab_max = functools.partial(aggregate_func,'max')
get_sqltab_min = functools.partial(aggregate_func,'min')
get_sqltab_sum = functools.partial(aggregate_func,'sum')
get_sqltab_avg = functools.partial(aggregate_func,'avg')

@db_wrapper
def get_sqltab_count(conn,table):
    if 'select' in table.lower():
        sql = f'select count(1) d from ({table}) as tb'
    else :
        sql = f'select count(1) d from {table}'
    cur = conn.cursor()
    cur.execute(sql)
    num = cur.fetchone()[0]
    cur.close()
    return num

def get_sqltabs_count(conn,tables,gt_num = 0):
    '''获取数据库表记录数
    
    Parameters
    --------------
    conn: DBAPI
        数据库连接对象
    tables: list
        表名列表
    Returns
    -------------
    dict
        {table:count}
    '''
    tables_num = {}
    for tb in tables:
        num = get_sqltab_count(conn,tb)
        tables_num[tb] = num
    if gt_num:
        tables_num = {k:v for k,v in tables_num.items() if v>=gt_num}
    return tables_num

def get_sqltab_count_diff(source_conn,target_conn,tables):
    '''获取源数据库和目标数据库表记录数差异

    Parameters
    ----------
    source_conn : DBAPI
        源数据库连接
    target_conn : DBAPI
        目标数据库连接
    tables : dict
        表名映射字典
    Returns
    -------
    dict
    '''
    source_num = get_sqltabs_count(source_conn,tables.keys())
    target_num = get_sqltabs_count(target_conn,tables.values())
    diff_num = {}
    for n in tables:
        if source_num[n]!=target_num[n]:
            diff_num[n] = (source_num[n],target_num[n])
    return diff_num

@db_wrapper
def get_sqltab_cols(conn,table = '',sql=''):
    '''获取数据库表字段
   
    Parameters
    --------------
    conn: DBAPI
        数据库连接对象
    table: str
        数据库表名 或sql语句
    sql: str
        自定义sql语句 
    Returns
    -------------
    list
    '''
    if 'select' in table.lower():
        get_sqlcols = f'select * from ({table}) a where 1=2 '
    else:
        get_sqlcols = f'select * from {table} a where 1=2 '
    cur = conn.cursor()
    cur.execute(get_sqlcols)
    cur.fetchall()
    cols = [col[0].upper() for col in cur.description]
    cur.close()
    return cols

@db_wrapper
def get_sqltab_values(conn,table,field='*'):
    '''获取数据库表字段值
    
    Parameters
    --------------
    conn:dbapi
    table:str
        表名
    sql:str
        自定义sql语句
    field:str
        字段名称 
    returns
    -------------
    list
        当未指定field时，返回第一个字段的值列表
    '''
    if 'select' in table.lower():
        sql = f'select {field} from ({table}) as tb'
    else:
        sql = f'select {field} from {table}'
    cur = conn.cursor()
    cur.execute(sql)
    values = [n[0] for n in cur.fetchall()]
    cur.close()
    return values

@db_wrapper
def get_sqltab_one(conn,table:str,**kwargs):
    if 'select' in table.lower():
        sql = f'select * from ({table}) as a '
    else:
        sql = f'select * from {table} a'

    sql_where = ' where '
    for k,v in kwargs.items():
        if isinstance(v,(list,tuple)):
            sql_where += f'{k} in {tuple(v)} and '
        elif isinstance(v,(dict)):
            for k1,v1 in v.items():
                sql_where += f'k {k1} {v1} and '
        else:
            sql_where += f'{k}={v} and '
    sql_where = sql_where[:-4]
    sql += sql_where

    cur = conn.cursor()
    cur.execute(sql)
    values = cur.fetchone()
    data = {}
    if values:
        cols = [col[0].upper() for col in cur.description]
        data = dict(zip(cols,values))
    cur.close()
    return data

@db_wrapper
def get_sqltab_all(conn,table:str,**kwargs):
    if 'select' in table.lower():
        sql = f'select * from ({table}) as a '
    else:
        sql = f'select * from {table} a'

    sql_where = ' where '
    for k,v in kwargs.items():
        if isinstance(v,(list,tuple)):
            sql_where += f'{k} in {tuple(v)} and '
        elif isinstance(v,(dict)):
            for k1,v1 in v.items():
                sql_where += f'k {k1} {v1} and '
        else:
            sql_where += f'{k}={v} and '
    sql_where = sql_where[:-4]
    sql += sql_where

    cur = conn.cursor()
    cur.execute(sql)
    cols = [col[0].upper() for col in cur.description]
    datas = []
    for values in cur:
        data = dict(zip(cols,values))
    datas.append(data)
    cur.close()
    return data

@db_wrapper
def get_sqltab_description(conn,table = '',sql=''):
    '''获取数据库表元数据
        
    Parameters
    --------------
    conn: PEP249 API
        数据库连接对象
    table: str
        数据库表名
    sql: str
        自定义sql语句 
    Returns
    -------------
    dict
        {columns:data_type}
    '''
    if 'select' in table.lower():
        sql = f'select * from ({table}) as a where 1=2'
    else:
        sql = f'select * from {table} a where 1=2'
    cur = conn.cursor()
    get_sqlcols = sql
    cur.execute(get_sqlcols)
    des = cur.description
    cur.fetchall()
    cur.close()
    return des

@db_wrapper
def sqltab_truncate(conn,table):
    '''清空数据
    '''
    cur = conn.cursor()
    cur.execute('truncate table '+table)
    conn.commit()
    cur.close()

@db_wrapper
def sql_execute(conn,sql):
    '''执行sql
    '''
    cur = conn.cursor()
    try:
        for s in sql.split(';'):
            if s.strip():
                cur.execute(s.strip())
        conn.commit()
    except Exception as e:
        print(e)
    cur.close()
    return True


@db_wrapper
def get_sqltab_names(conn,db,sql = '',full_name = False,upper = False):
    '''所有表名列表 sql第一列返回表名称 {db}
    '''
    try:
        from sqlalchemy import MetaData
        engine = sqlalchemy_engine(conn)
        metadata = MetaData()
        metadata.reflect(bind=engine,schema=db)
        all_table = [table_name for table_name in metadata.tables]
    except Exception as e:
        if not sql:
            raise '自动反射表失败 请使用sql查询表名称!'
        cur = conn.cursor(sql.format(db = db))
        cur.execute(sql)
        all_table = [n[0] for n in cur.fetchall()]
        cur.close()

    if not full_name:
        all_table = [n.upper().replace(db.upper()+'.','') for n in all_table if n]
    
    if not upper:
        all_table = [n.lower() for n in all_table if n]
        
    return list(set(all_table))

def get_sqltab_pk(conn,db,table):
    '''所有表的主键名称
    '''
    from sqlalchemy import MetaData
    engine = sqlalchemy_engine(conn)
    metadata = MetaData()
    metadata.reflect(bind=engine,schema=db,only=[table])
    tb = metadata.tables[table]
    return tb.primary_key