
import datetime as dt
from inspect import isfunction
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED,FIRST_COMPLETED, as_completed
import time
import threading
from .utils.general import pep249_paramstyle_format,pep249_paramstyle
from .utils.sqltab import get_sqltab_cols,get_sqltab_max,sqltab_truncate
from .source import source_sql
from .table import table_basic
from .utils.sqltab import get_sqltab_names,get_sqltabs_count
try:
    from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn,MofNCompleteColumn
    progress = Progress(TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        MofNCompleteColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        TimeRemainingColumn(),
                        TextColumn("•"),
                        TimeElapsedColumn(),
                      )
except ImportError:
    progress = None
    
# 创建线程锁，用于线程安全的进度条更新
lock = threading.Lock()

def sqlsync(source_conn,source_table,target_conn,target_table,columns:list = [],pks:list= [],rename={},batch_size=50000,opfield='',between =(),truncate=False,before_sql='',after_sql='',connect_close =False,task=False,table_cls = table_basic,update = False,fields_adapter={},include_values={},exclude_values={},backup=None,rich=True,**kwargs):
    '''数据库表同步 默认为追加模式

    Parameters
    -------------------
    source_conn:PEP249 API
        源数据库连接
    source_table:str
        源表表名
    target_conn:PEP249 API
        目标数据库连接
    target_table:str
        目标表表名
    columns:list
        字段名称 未指定字段时 将自动从数据库获取字段
    batch_size:int
        批量提交记录数
    pks:list
        主键
    rename:dict
        字典
    opdate_field:str
        增量日期字段名称
    update:bool
        当数据已经存在时 指定更新或者跳过 True 更新 False 跳过 默认为False
    truncate:bool
        是否清空表 默认 False
    before_sql:str
        初始化执行的sql
    after_sql:str
        操作完成后执行的sql

    Examples
    ---------
    
    '''
    # 进行数据备份
    if isfunction(backup):
        backup(target_table)

    if 'select' in source_table.lower():
        source_query = f'select * from ({source_table}) a '
    else:
        source_query = 'select * from '+source_table+' '

    # 读取数据源连接 处理为标准连接 供后续使用
    src_field = get_sqltab_cols(source_conn,source_table)
    # 写入数据源连接 保持传入连接对象
    tag_field = get_sqltab_cols(target_conn,target_table)

    src_field = [n.upper() for n in src_field]
    rename = {k.upper():v for k,v in rename.items()}
    columns = columns if columns else tag_field
    columns = [n.upper() for n in columns]
    columns = [n for n in columns if rename.get(n,n) in src_field]
    
    if not columns:
        raise ValueError(columns,'映射字段为空！')
        
    if between:
        src = source_sql(source_conn,source_query,between)
    else:
        src = source_sql(source_conn,source_query)
    if before_sql and '{}' in before_sql:
        before_sql = before_sql.format(source_table)
    if after_sql and '{}' in after_sql:
        after_sql = after_sql.format(source_table)
    target = table_cls(target_conn,target_table,columns = columns,pks = pks,batch_size = batch_size,rename = rename,truncate =truncate,init_sql=before_sql,end_sql=after_sql,include_values=include_values,exclude_values=exclude_values,fields_adapter=fields_adapter,**kwargs)
    if before_sql:
        print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' 初始化sql影响行数: ' + str(target.rowcount))

    if src.rowcount==0:
        return True
    if progress and rich:
        if task:
            progress.update(task,total = src.rowcount)
            progress.start_task(task)
            try:
                for row in src:
                    if pks and not truncate:
                        target.ensure(row,update = update)
                    else:
                        target.insert(row,rename = rename)
                        progress.update(task, advance = 1)
                target.endload()
            except Exception as e:
                progress.update(task, visible=False)
                print(f"Error in {task}: {e}")
        else:
            task_id = progress.add_task("[green]{}".format(target.table_name.lower()), total=src.rowcount)
            with progress:
                try:
                    for row in src:
                        if target.all_row_num and target.all_row_num % batch_size == 0:
                            with lock:
                                progress.update(task_id, advance = batch_size)
                        if pks and not truncate:
                            target.ensure(row)
                        else:
                            target.insert(row,rename = rename)
                    
                    target.endload()
                    with lock:
                        if batch_size>src.rowcount:
                            progress.update(task_id, advance = src.rowcount)
                        else:
                            progress.update(task_id, advance = target.all_row_num % batch_size)
                except Exception as e:
                    with lock:
                        progress.update(task_id, visible=False)
                        print(f"Error in {target.table_name}: {e}")
            progress.remove_task(task_id)

    else:
        for row in src:
            if pks and not truncate:
                target.ensure(row)
            else:
                target.insert(row,rename = rename)
            if target.all_row_num % batch_size == 0:
                print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Insert row: ' + str(target.insert_row_num) + ' update row: ' + str(target.update_row_num))
        target.endload()
        print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Insert row: ' + str(target.insert_row_num) + ' update row: ' + str(target.update_row_num))

    if connect_close:
        try:
            target_conn.close()
            source_conn.close()
        except Exception as e:
            pass
    return True

def dbsync(source_conn,target_conn,db=None,config={},config_merge = {},include =[],exclude =[],max_workers=3,fields_adapter={},table_cls = table_basic,**kwargs):
    '''数据库同步
    
    Parameters
    -----------
    source_conn:
        源数据连接
    target_conn:
        目录数据源连接
    db:str
        当未提供config 使用sqlalchemy自动解析表时需要指定数据库名称 
    config:dict
        表映射配置 以源表名为键 具体可配置值参考 sqlsync 函数 对每个表进行单独配置
        {source_table :{target_table:'',batch:1000,...}}
    include:list
        列出仅需要同步的表名
    exclude:list
        需要排除的表名
    fields_adapter:dict
        字段适配器
    **kwargs
        其他参数参考 sqlsync 函数 
    '''

    # 未指定映射表配置时 使用sqlalchemy自动解析出同名表
    if not config:
        if not db:
            raise ValueError('采用自动反射表的方式，必须指定数据库（db）参数!')
        print('自动检测表...')
        tabs = get_sqltab_names(source_conn,db)

        tabs = set(tabs)
        print('检测表数量',len(tabs))
        #tabs = get_sqltabs_count(source_conn,tabs,gt_num=1)
        config = {str(n).upper():{'target_table':str(n).upper()} for n in tabs}
    
    # 合并配置
    config_merge = {k.upper():v for k,v in config_merge.items()}
    for n in config_merge:
        config[n] = {**config.get(n,{}),**config_merge[n]}
    # 未指定同步配置时 使用默认配置
    exclude = [n.upper() for n in exclude]
    include = [n.upper() for n in include]

    if exclude:
        for tab in exclude:
            if tab in config:
                del config[tab]
        
    if include:
        config = {k:v for k,v in config.items() if k in include}
    
    print('同步表数量',len(config))
    if isfunction(source_conn) and isfunction(target_conn):
        #import sqlalchemy.pool as pool
        #source_conn_pool = pool.QueuePool(source_conn, max_overflow = max_overflow,pool_size = pool_size)
        #target_conn_pool = pool.QueuePool(target_conn, max_overflow = max_overflow,pool_size = pool_size)
        if progress:
            print('开启并发运行...')
            with progress:
                with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    task_all = []
                    for source_table,tag_table_args in config.items():
                        task_id = progress.add_task("[green]{}".format(tag_table_args['target_table'].lower()),total=None,start=False)
                        task_all.append(executor.submit(sqlsync,
                                        source_conn = source_conn,
                                        source_table = source_table,
                                        target_conn = target_conn,
                                        target_table = tag_table_args.pop('target_table'),
                                        connect_close = tag_table_args.pop('connect_close',True),
                                        task = task_id,
                                        fields_adapter = fields_adapter,
                                        table_cls = table_cls,
                                        **{**kwargs,**tag_table_args}
                                        ))
                    while not all(f.done() for f in task_all):
                        progress.refresh()  # 手动刷新进度条
                        time.sleep(0.5)
                    
    else:
        for source_table,tag_table_args in config.items():
            sqlsync(source_conn = source_conn,
                    source_table = source_table,
                    target_conn = target_conn,
                    target_table = tag_table_args.pop('target_table'),
                    connect_close = tag_table_args.pop('connect_close',True),
                    fields_adapter = fields_adapter,
                    table_cls = table_cls,
                    **{**kwargs,**tag_table_args}
                    )

