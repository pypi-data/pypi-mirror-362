
import datetime as dt
from subprocess import run
from .source import source_pandas,source_sql,source_csv
from .table import table_basic
from .utils.sqltab import sqltab_truncate

__all__ = ['csvldr','pandasldr','sqlldr']

def pandasldr(conn,table,dataframe,batch_size = 10000,del_cols = [],pks = [],ensure=False,logger = None,truncate = False,table_cls=table_basic,**kwargs):
    '''
    将pandas的DataFrame数据加载到数据库中
    
    Parameters:
    ----------
    conn : PEP249 API
        数据库连接对象
    table : str
        目标数据库表名
    dataframe : pandas.DataFrame
        需要导入的DataFrame对象
    batch_size : int, 默认10000
        每批次提交的记录数,用于控制内存使用
    del_cols : list, 默认[]
        需要排除的DataFrame列名列表
    pks : list, 默认[]
        主键字段列表
    ensure : bool, 默认False
        是否检查记录存在(True则更新,False则插入)
    logger : logging.Logger, 默认None
        日志记录器,None时使用print输出
    truncate : bool, 默认False
        是否在导入前清空目标表
    table_cls : class, 默认table_basic
        表操作类
    **kwargs : dict
        其他参数

    Return:
    -------
    bool
        导入成功返回True
    '''

    if logger:
        output = logger
    else:
        output = print
        
    df = dataframe.where(dataframe.notnull(), None)
    source_data = source_pandas(df)
    table_metdata = source_sql(conn,'select * from '+table)
    cols = [n for n in table_metdata.cols if n in source_data.cols]

    tag_table = table_cls(conn,table,columns = cols,pks = [],batch_size = batch_size,del_cols=del_cols,**kwargs)

    if truncate and not ensure:
        sqltab_truncate(conn,table)
        output(dt.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ),'【{}】清空'.format(table))

    num = 0
    for row in source_data:
        num+=1
        if ensure:
            tag_table.ensure(row)
        else:
            tag_table.insert(row)
        if num % batch_size == 0:
            output(dt.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ),'【{}】insert line number:'.format(table),num)
    tag_table.endload()
    output(dt.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ),'【{}】insert line number:'.format(table),num)
    return True

def csvldr(conn,table,file,batch_size =30000,encoding = 'utf-8',pks = None,ensure=False,to_datetime = None,del_cols = None,truncate=False,table_cls = table_basic,**kwargs):
    '''将文本数据导入数据库

    Parameters
    ------------
    conn:pep249 API
        标准数据库连接
    table:str
        数据库表名
    file:str
        文件路径
    batch_size：int
        每次批量加载数量
    encoding:str
        文件编码
    date_col:list
        需要从文本转为日期的字段名称
    del_cols:list
        需要排除字段
    truncate:bool
        清空表模式
    '''
    to_datetime =  to_datetime if to_datetime else []
    del_cols = del_cols if del_cols else []
    pks = pks if pks else []

    source_data = source_csv(file,encoding = encoding,to_datetime = to_datetime)
    cols = [n for n in source_data.fieldnames if n in source_data.fieldnames]
    tag_table = table_cls(conn,table,columns = cols,batch_size = batch_size,pks=pks,del_cols=del_cols,**kwargs)
    if truncate and not ensure:
        sqltab_truncate(conn,table)
        print(dt.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ),'【{}】清空'.format(table))

    num = 0
    for row in source_data:
        num+=1
        if ensure:
            tag_table.ensure(row)
        else:
            tag_table.insert(row)

        if num % batch_size == 0:
            print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'【{}】insert line number:'.format(table),num)
            conn.commit()
    tag_table.endload()
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'【{}】insert line number:'.format(table),num)
    
def sqlldr(user= None,control = None,log = None,bad =None,data = None,discard =None,discardmax = None,skip = None,load =None,errors = None,rows = None,
           bindsize =None,silent = None,direct = None,parfile = None,parallel = None,file =None,skip_unusable_indexes = None,skip_index_maintenance = None,
           commit_discontinued = None,readsize=None):
    '''sqlldr python封装

    example:
    ----------
    sqluldr2(user = 'user/password@127.0.0.1:1521/orcl',query='table')
    '''
    kwargs = locals()
    args = []
    for k,v in kwargs.items():
        if v:
            args.append('{}={}'.format(k,v))
    if args:
        command = 'sqlldr ' +' '.join(args)
        return run(command,capture_output = True,text = True)
