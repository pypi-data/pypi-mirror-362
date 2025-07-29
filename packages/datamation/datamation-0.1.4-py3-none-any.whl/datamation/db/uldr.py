
import gzip
import sys
import csv
import datetime as dt
import time
import locale
import subprocess
from pathlib import Path
from .source import source_sql

__all__ = ['dbuldr','dump_sql','sqluldr2','dump_csv']

def dbuldr(conn,sql:str='',table_name:str='',save_file = '',output:str='csv',
           db_type = 'postgres',
           date_format = '%Y-%m-%d %H:%M:%S',
           escape_str = True,
           batch_size = 50000,
           insert_batch_size = 1,
           fieldsep=',',
           rowsep='\n\r',
           encoding = 'utf-8',
           included_head = True,
           archive = True):
    
    if output=='csv':
        return dump_csv(conn,sql,file = save_file,batch_size=batch_size,fieldsep=fieldsep,rowsep=rowsep,encoding=encoding,included_head=included_head,archive=archive)
    if output=='sql':
        return dump_sql(conn, table_name,save_file=save_file,db_type=db_type,date_format=date_format,escape_str=escape_str,batch_size=batch_size)

def dump_csv(conn,sql='',save_file = None,batch_size = 50000,fieldsep=',',rowsep='\n\r',encoding='utf-8',included_head=True,archive =True):
    '''数据导出
    不同的数据库可能需要一些单独的方法在连接或者游标层处理一些特殊的数据类型 
    例oracle的cx_Oracle clob对象返回的并不是直接字符串 需要使用相应方法进行提取
    def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
            if defaultType == oracle.CLOB:
                return cursor.var(oracle.LONG_STRING, arraysize = cursor.arraysize)
    conn.outputtypehandler = OutputTypeHandler

    Parameters
    ------------
    conn:PEP249 API
    sql: str
        sql
    file:str
        文件名称
    batch_size:int
        批量加载行数
    delimiter:str
        字段分隔符 默认 ','
    encoding:str
        文件编码 默认utf-8
    db:str
        oracle、
        数据库类型
    archive:bool
        是否压缩文件 默认为True
    '''
    src = source_sql(conn,sql,data_format='list')
    data = []
    row_num = 0
    
    save_file = save_file if save_file else sql[:50]
    save_file = dt.datetime.now().strftime('%Y%m%d') + '_' + save_file

    if save_file.split('.')[-1] in ['GZ','gz'] or archive:
        file_obj = gzip.open
    else:
        file_obj = open

    head = src.cols
    with file_obj(save_file, 'wt', newline=rowsep,encoding=encoding) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=fieldsep,lineterminator = '\r\n' ,quoting=csv.QUOTE_NONNUMERIC)
        if included_head:
            spamwriter.writerow(head)
        for n in src:
            data.append(n)
            if len(data) % batch_size == 0:
                row_num+=batch_size
                print(time.ctime(),'out row {}'.format(row_num))
                spamwriter.writerows(data)
                csvfile.flush()
                data = []
        if data:
            row_num+=len(data)
            spamwriter.writerows(data)
            print(time.ctime(),'out row {}'.format(row_num))
            data = []
    return True

def dump_sql(
    table_name,
    conn=None,
    source_obj=None,
    db_type='postgres',
    date_format='%Y-%m-%d %H:%M:%S',
    insert_batch_size=1,
    escape_str=True,
    save_path='',
    compression=False,
):
    """
    通用的 SQL INSERT 语句生成器，支持 PostgreSQL、MySQL、Oracle。
    
    支持：
    - 传 source_sql 查询后的对象 (source_obj)，优先使用
    - 或传 conn，从数据库查询
    - 批量写入
    - 压缩写入

    Parameters
    ----------
    table_name : str
        目标表名，不能为空。
    conn : PEP 249 兼容的数据库连接对象，可选。
        如果提供了 source_obj，则不需要此参数。
    source_obj : object, 可选
        已查询的对象，必须有 `cols` 属性，包含列名。
        如果未提供，则从 `conn` 查询。
    db_type : str, 可选 
        数据库类型，支持 'postgres', 'mysql', 'oracle'。默认为 'postgres'。
    date_format : str, 可选
        日期格式化字符串，默认为 '%Y-%m-%d %H:%M:%S'。
    insert_batch_size : int, 可选
        每次插入的行数，默认为 1。
    escape_str : bool, 可选
        是否对字符串进行转义，默认为 True。
    save_path : str, 可选
        保存 SQL 文件的路径，默认为当前工作目录。
    compression : bool, 可选
        是否对输出文件进行 gzip 压缩，默认为 False。
    """
    if not table_name:
        raise ValueError("表名不能为空")
    
    # 优先使用 source_obj
    if source_obj is not None:
        if not hasattr(source_obj, 'cols'):
            raise ValueError("source_obj必须有cols属性")
        cols = source_obj.cols
        rows = source_obj
    else:
        if not conn:
            raise ValueError("未提供 source_obj，也未提供数据库连接 conn")
        # 这里调用 source_sql 生成实例
        source_obj = source_sql(conn, f'SELECT * FROM {table_name}', data_format='list')
        if not source_obj:
            return []
        cols = source_obj.cols
        rows = source_obj

    if not rows:
        return []

    escape_prefix = {
        'postgres': "'",
        'mysql': "'",
        'oracle': "'"
    }
    base_sql = f'INSERT INTO {table_name} ({",".join(cols)}) VALUES '

    # 构造保存路径
    if save_path and not Path(save_path).is_dir():
        # 如果是文件，取其父目录作为保存路径
        sql_file_path = Path(save_path)
        save_path = Path(save_path).parent
        save_path.mkdir(parents=True, exist_ok=True)
    else:
        base_path = Path(save_path).resolve() if save_path else Path.cwd()
        base_path.mkdir(parents=True, exist_ok=True)
        sql_filename = f"{table_name}.sql"
        sql_file_path = base_path / sql_filename
    file_writer = None

    try:
        # 打开文件（gzip或普通文本）
        if compression:
            sql_file_path = sql_file_path.with_suffix('.sql.gz')
            file_writer = gzip.open(sql_file_path, 'wt', encoding='utf-8')
        else:
            file_writer = open(sql_file_path, 'w', encoding='utf-8')

        # 写入数据
        batch = []
        for idx, row in enumerate(rows):
            if isinstance(row, dict):
                row = [row.get(col) for col in cols]
            row_values = []
            for value in row:
                if isinstance(value, dt.datetime):
                    formatted_date = value.strftime(date_format)
                    row_values.append(f"'{formatted_date}'")
                elif value is None:
                    row_values.append('NULL')
                elif isinstance(value, (float, int)):
                    row_values.append(str(value))
                elif isinstance(value, str):
                    if escape_str:
                        value = value.replace("'", "''")
                        use_prefix = escape_prefix.get(db_type, "'")
                        if db_type == 'postgres' and any(x in value for x in ['\\', '\n', '\t']):
                            use_prefix = "E'"
                        row_values.append(f"{use_prefix}{value}'")
                    else:
                        row_values.append(f"'{value}'")
                else:
                    row_values.append(f"'{str(value)}'")

            batch.append(f"({','.join(row_values)})")

            if (idx + 1) % insert_batch_size == 0 or idx + 1 == len(rows):
                insert_stmt = base_sql + ',\n'.join(batch) + ';'
                file_writer.write(insert_stmt + '\n')
                batch = []

    finally:
        if file_writer:
            file_writer.close()

    return str(sql_file_path.absolute())


def sqluldr2(user=None,query=None,sql=None,field = None,record = None,rows = None,file = None,log = None,
             fast = None,text = None,charset = None,ncharset = None,parfile = None,read = None,sort = None,hash = None,array = None,head =None,batch = None,size = None,
             serial = None,trace = None,table = None,control = None,mode = None,buffer = None,long = None,width = None,quote = None,data = None,alter = None,safe = None,
             crypt=None,sedf = None,null = None,escape = None,escf = None,format = None,exec = None,prehead = None,rowpre = None,rowsuf = None,colsep = None,presql =None,
             postsql = None,lob = None,lobdir = None,split = None,degree = None,hint = None,unique = None,update = None,parallel=None,skip = None,skipby = None,skipby2 = None,):
    '''sqluldr2 python封装
    sqluldr2是oracle的sqlldr的python封装 用于导出数据 与sqlldr的参数基本一致 但是有一些参数不支持 例如direct 、parallel

    Examples
    ---------
    sqluldr2(user='test',query='select * from test',file='test.csv',field='id,name',record='|',rows='|',head='Y',batch='Y',size=10000,mode='insert',buffer=100000,lob='Y',lobdir='lob',split='Y',degree=4,unique='id',update='name')
    '''
    kwargs = locals()
    args = []
    for k,v in kwargs.items():
        if v:
            args.append('{}={}'.format(k,v))
    if args:
        command = 'sqluldr2 ' +' '.join(args)
        return subprocess.run(command,capture_output=True,text = True)
    
