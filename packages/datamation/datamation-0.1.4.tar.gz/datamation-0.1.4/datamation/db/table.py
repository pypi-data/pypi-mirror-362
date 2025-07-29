#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import import_module
from collections import OrderedDict
import collections
from functools import lru_cache
from itertools import chain
import itertools
import concurrent.futures
import inspect
from inspect import isfunction
from pathlib import Path
import abc
import uuid
import sys
from types import MethodType
import time 
from ..log import get_logger
from .utils.general import inference_dtype
from .source import source_sql
from .cache import Cache_database,Cache_database
from .utils.transform import Tupper,Tlower,Tpairwise_seq

__all__ = ['table_basic','Dimension','FactTable','Change_slowly','Cache_table','elastic_basic']

log = get_logger('db')
log.setLevel(50)

class BatchOperator:
    def __init__(self, batch_size=50000, strict=True):
        self.batch_size = batch_size
        self.batch_insert = []
        self.batch_update = []
        self.batch_delete = []
        self.all_row_num = 0
        self.err_row_num = 0
        self.insert_row_num = 0
        self.update_row_num = 0
        self.delete_row_num = 0
        self.data_traffic = 0
        self.err_rows = collections.defaultdict(list)
        self.strict = strict

    @property
    def is_batch_suffice(self):
        '''当前批量是否满足提交数量'''
        return (len(self.batch_update)+len(self.batch_insert)+len(self.batch_delete)) % self.batch_size == 0

    def _batch_append(self, row, mode):
        if any(row):
            if mode=='insert':
                self.insert_row_num+=1
                self.all_row_num+=1
                self.batch_insert.append(row)
            if mode=='update':
                self.update_row_num+=1
                self.all_row_num+=1
                self.batch_update.append(row)
            if mode =='delete':
                self.delete_row_num+=1
                self.all_row_num+=1
                self.batch_delete.append(row)

class Table(BatchOperator, metaclass=abc.ABCMeta):
    def __init__(self,table_name='',columns=[],pks=[],up_columns=[],lookup_columns =[],batch_size=50000,fieldmap={},rowmap={},
                 rename={},del_cols = [],char_format = 'upper',default_values = {},include_values ={},exclude_values ={},
                 strict = True,truncate = False,thread_count = 1,parallel=False,fields_adapter ={}):
        '''增删改查

        Parameters
        ---------------
        table_name:str
            数据库表名
        columns:list
            字段名
        pks:list
            Primary key 主键
        up_columns:list
            指定更新的字段
            默认 up_columns = columns
        lookup_columns:list
            指定可以作为查询条件的字段
        batch_size:int
            指定批量提交的行数
        fieldmap:dict
            字段值转换 {fieldname:function}
        rowmap:function
            行处理函数 接受一个dict入参 dict为键值对的行数据 返回一个dict
        del_cols:list
            指定删除的字段
        char_format:str
            upper、lower 默认 None
            指定字段名称格式化为大写或者小写
        default_values:dict
            指定默认值 {fieldname:value}
        strict:bool
            默认 True 遇到错误正常报错 
            False 跳过异常数据行 异常记录在err_rows属性中
        truncate:bool
            default False 指定是否清空表
        thread_count:int
            实际批量写数据时 使用线程数为 thread_count-1 会保留一个连接作为主连接使用
            所以多线程最小为3 这时会使用2个线程进行批量数据处理
        fields_adapter :dict
            指定值类型转换 {type:function}

        '''
        if char_format =='upper':
            t_char = Tupper
        elif char_format == 'lower':
            t_char = Tlower
        else:
            t_char = lambda x:x

        self.parallel = parallel
        # 标准化清理
        columns = [t_char(n) for n in columns]
        pks = t_char(pks) if isinstance(pks,str ) else [t_char(n) for n in pks]
        up_columns = [t_char(n) for n in up_columns]
        del_cols = [t_char(n) for n in del_cols]
        rename = {t_char(k) : t_char(v) for k,v in rename.items()}

        self.include_values = {t_char(k) : v for k,v in include_values.items()}
        self.exclude_values = {t_char(k) : v for k,v in exclude_values.items()}

        default_values = {t_char(k):v for k,v in default_values.items()}
       
        for n in default_values:
            if n not in columns:
                columns.append(n)

        self.thread_count = thread_count
        self.char_format = char_format
        self.default_values = default_values
        self.strict = strict
        self.truncate = truncate
        self.t_char = t_char

        self.del_cols = tuple(t_char(n) for n in del_cols)
        self.columns = tuple(n for n in columns if not t_char(n) in self.del_cols)
        self.columns_all = [t_char(n) for n in self.columns]
        for n in pks:
            if n  not in self.columns_all:
                self.columns_all.append(n)

        self.table_name = t_char(table_name)
        self.columns_all = tuple(self.columns_all)
        self.lookup_columns = tuple(t_char(n) for n in lookup_columns)
        self.pks = tuple(t_char(n) for n in pks)
        
        self.fieldmap = fieldmap
        self.rowmap = rowmap
        self.up_columns = tuple(up_columns) if up_columns else tuple(n for n in columns if n not in self.pks)

        super().__init__(batch_size=batch_size, strict=strict)
        self.rename = rename
        self.fields_adapter = fields_adapter

    def row_name_format(self,row):
        try:
            return {self.t_char(k):v for k,v in row.items()}
        except Exception as e:
            print('异常',row)
            raise e
        
    def pipeline(self,row,rename ={}):  
        if rename or self.rename:
            row = self.row_rename(row,rename)

        if self.include_values:
            for k,v in self.include_values.items():
                if isinstance(v, (list, tuple)):
                    if row.get(k) not in v:
                        return {}
                else:
                    if row.get(k) != v:
                        return {}

        if self.exclude_values:
            for k,v in self.exclude_values.items():
                if isinstance(v, (list, tuple)):
                    if row.get(k) in v:
                        return {}
                else:
                    if row.get(k) == v:
                        return {}
        
        if self.fields_adapter:
            for k,v in row.items():
                for fk,fv in self.fields_adapter.items():
                    if isinstance(row[k],fk):
                        row[k] = fv(row[k])

        row = self.field_transform(row)
        row = self.row_transform(row)
        row = self.transform(row)
        row = self.row_name_format(row)
        return row
    
    def insert(self,row,rename ={}):
        row = self.pipeline(row,rename)
        self._batch_append(row,'insert')

    def delete(self,row,rename={}):
        row = self.pipeline(row,rename)
        self.delete_row_num+=1
        self.all_row_num+=1
        self._batch_append(row,'delete')

    def update(self,row,ori_row={},rename={}):
        row = self.pipeline(row,rename)
        if not ori_row:
            ori_row = self.lookup(row)
        ori_row.update(row)
        self._batch_append(ori_row,'update')

    def lookup(self,row,rename={}):
        pass

    def ensure(self,row,rename={},update = True):
        ori_row = self.lookup(row)
        if ori_row:
            if update:
                return self.update(row,ori_row = ori_row,rename = rename)
        else:
            return self.insert(row,rename = rename)

    @abc.abstractmethod
    def load(self):
        pass

    def endload(self):
        self.load()

    @abc.abstractmethod
    def standardization(self,row):
        '''数据标准化'''
        return row

    @property
    def is_batch_suffice(self):
        '''当前批量是否满足提交数量'''
        return (len(self.batch_update)+len(self.batch_insert)+len(self.batch_delete)) % self.batch_size == 0

    def _batch_append(self,row,mode):
        new_row = self.standardization(row)
        if any(new_row):
            if mode=='insert':
                self.insert_row_num+=1
                self.all_row_num+=1
                self.batch_insert.append(new_row)
            if mode=='update':
                self.update_row_num+=1
                self.all_row_num+=1
                self.batch_update.append(new_row)
            if mode =='delete':
                self.batch_delete.append(new_row)

            if self.is_batch_suffice:
                self.data_traffic = (sys.getsizeof(self.batch_insert)+sys.getsizeof(self.batch_update)+sys.getsizeof(self.batch_delete))/1024/1024
                if self.strict:
                    self.load()
                else:
                    try:
                        self.load()
                    except Exception as e:
                        pass

    def field_transform(self,row):
        '''字段处理方法'''
        if self.fieldmap:
            for k,func in self.fieldmap.items():
                if k in row:
                    row[k] = func(k,row[k],row)
        # 更新默认值
        for k,v in self.default_values.items():
            if not row.get(k,None):
                row[k] = v

        return row

    def row_transform(self,row):
        '''行处理方法
        '''
        if hasattr(self.rowmap, '__call__'):
            return self.rowmap(row)
        return row  
        
    def row_rename(self,row,rename={}):
        '''字段名称重命名'''
        if self.rename:
            row = {self.rename.get(self.t_char(n),n):v for n,v in row.items()}

        if rename:
            rename = {self.t_char(k):v for k,v in rename.items()}
            row = {rename.get(self.t_char(n),n):v for n,v in row.items()}
        return row

    def transform(self, row):
        '''动态绑定自定义的行处理函数
        '''
        for decorator in getattr(self, '_transform_decorators', []):
            row = decorator(row)
        return row

    def add_transform_decorator(self, decorator):
        '''添加行处理装饰器
        
        Parameters
        ---------------
        decorator: callable
            接受一个row参数的可调用对象，返回处理后的row
        '''
        if not hasattr(self, '_transform_decorators'):
            self._transform_decorators = []
        self._transform_decorators.append(decorator)

    @property
    def complete(self):
        '''完整性验证 数据操作无异常时返回True
        '''
        return self.all_row_num == self.all_row_num - self.err_row_num

    def diff(self,row,old_row):
        '''行差异检查'''
        diff = set()
        local_row = {self.t_char(k):v for k,v in row.items() if self.t_char(k) in self.columns_all}
        local_old_row = {self.t_char(k):v for k,v in old_row.items()}

        for n in local_row:
            if local_row.get(n,None) !=None and str(local_row.get(n,None))!=str(local_old_row.get(n,None)):
                diff.add(n)
        return diff
    
    def row_diff_reset(self,row,old_row):
        '''行差异重置'''
        local_row = {self.t_char(k):v for k,v in row.items() if self.t_char(k) in self.columns_all}
        local_old_row = {self.t_char(k):v for k,v in old_row.items()}
        for k,v in local_old_row.items():
            if local_row.get(k,None) and str(local_old_row.get(k,None))!=str(v):
                local_row[k] = v
        return local_row

    def general_execute(self,*args,**kwargs):
        '''普通执行'''
        pass

    @abc.abstractmethod
    def general_executemany(self,*args,**kwargs):
        '''普通批量执行'''
        pass

    def parallel_execute(self,*args,**kwargs):
        '''并行执行'''
        pass
    
    def parallel_executemany(self,*args,**kwargs):
        '''并行批量执行'''
        pass

    def execute(self,*args,**kwargs):
        if self.parallel:
            self.general_execute(*args,**kwargs)
        else:
            self.general_execute(*args,**kwargs)

    def executemany(self,*args,**kwargs):
        if self.parallel:
            self.parallel_executemany(*args,**kwargs)
        else:
            self.general_executemany(*args,**kwargs)
        
class connect_wrapper(object):
    def __init__(self,connection,strict = True):
        ''' 数据库连接池 当存在sqlalchemy模块时使用连接池 否则回退到单连接
        '''
        self.lastrowid = None
        self.strict = strict
        self.err_rows = collections.defaultdict(list)
        self.conn_pool= None
        if not callable(connection) or hasattr(connection,'cursor'): 
            conn = lambda :connection
            self.thread_count = 1
        else:
            conn = connection
        try:
            import sqlalchemy.pool as pool
            self.conn_pool = pool.QueuePool(conn,max_overflow = 2, pool_size=self.thread_count,reset_on_return=False)
        except Exception as e:
            self.conn = conn()

        self.parallel_executor = concurrent.futures.ThreadPoolExecutor(max_workers =self.thread_count)

    def general_execute(self,operation,seq=None):
        conn = self.conn_pool.connect() if self.conn_pool else self.conn
        cursor = conn.cursor()
        try:
            for _ in range(3):
                try:
                    cursor.execute(operation,seq)
                    self.rowcount = cursor.rowcount
                    conn.commit()
                except Exception as e:
                    try:
                        conn.rollback()
                        cursor = conn.cursor()
                        cursor.close()
                    except Exception as e:
                        conn = self.conn_pool.connect() if self.conn_pool  else self.conn
                        cursor = conn.cursor()
                        continue
                    raise e
                break
            if hasattr(cursor,'lastrowid'):
                self.lastrowid = cursor.lastrowid
            else:
                self.lastrowid = None
        except Exception as e:
            if self.strict:
                raise e # 重新抛出异常
            else:
                self.err_rows[e].append((operation,seq))
                pass
        finally:
            # 释放资源
            conn.commit()
            cursor.close()
            if self.conn_pool:
                conn.close()

    def general_executemany(self,operation,seq):
        conn = self.conn_pool.connect() if self.conn_pool  else self.conn
        cursor = conn.cursor()
        # 如果数据执行失败，则回滚所有数据
        try:
            for _ in range(3):
                try:
                    cursor.executemany(operation,seq)
                    if not cursor.rowcount:
                        print('数据插入失败 数据库未变化 请检查数据格式...')
                        print(seq[:1])
                    break
                except Exception as e:
                    if _ == 2:
                        print('异常:',e)
                        print('异常数据:',operation,seq[:1])
                        raise e
                    try:
                        conn.rollback()
                        if self.conn_pool:
                            conn.close()
                    finally:
                        conn = self.conn_pool.connect() if self.conn_pool  else self.conn
                        cursor = conn.cursor()
                        
            if hasattr(cursor,'lastrowid'):
                self.lastrowid = cursor.lastrowid
            else:
                self.lastrowid = None
            conn.commit()

        except Exception as e:
            if self.strict:
                raise e
            else:
                self.err_rows[e].append((operation,seq))
                pass
        finally:
            # 释放资源
            cursor.close()
            if self.conn_pool:
                conn.close()

    def parallel_execute(self,operation,seq):
        '''并行执行sql语句'''
        self.parallel_executor.submit(self.general_execute,operation,seq)

    def parallel_executemany(self,operation,seq):
        '''并行执行sql语句'''
        spilt = Tpairwise_seq(list(range(len(seq))[::int(len(seq)/self.thread_count)]) + [len(seq)])
        with concurrent.futures.ThreadPoolExecutor(max_workers =self.thread_count) as e:
            for data in spilt:
                e.submit(self.general_executemany,operation,seq[data[0]:data[1]])
            #self.parallel_executor.submit(self.general_executemany,operation,seq[data[0]:data[1]])
            
    def executemany_possible(self,operation,seq):
        import queue
        q = queue.Queue()
        # 将数据二分放入队列
        q.put(seq[:len(seq)//2])
        q.put(seq[len(seq)//2:])

        # 错误行超过1万时，放弃重试 抛出异常
        for _ in range(len(seq)):
            try:
                # 当队列为空时，跳出循环
                if q.empty():
                    break
                seq = q.get()
                self.executemany(operation,seq)
            except Exception as e:
                # 当数据长度为1时，放弃重试
                if self.err_row_num>1000:
                    raise e
                if len(seq)==1:
                    self.err_rows[e].append(seq[0]) # 将错误数据放入错误数据字典
                    self.err_row_num+=1
                    continue
                q.put(seq[:len(seq)//2])
                q.put(seq[len(seq)//2:])
    
    def fetchone(self,operation,seq=None):
        # 获取单行数据
        conn = self.conn_pool.connect() if self.conn_pool  else self.conn
        cursor = conn.cursor()
        try:
            cursor.execute(operation,seq)
            res_row = cursor.fetchone()
            if res_row and not isinstance(res_row,dict):
                res_row = dict(zip([n[0] for n in cursor.description],res_row))
            return res_row
        except Exception as e:
            raise Exception(e,operation,seq)
        finally:
            cursor.close()
            if self.conn_pool:
                conn.close()

    def fetchall(self,operation,seq=None):
        # 获取所有行数据
        conn = self.conn_pool.connect() if self.conn_pool  else self.conn
        cursor = conn.cursor()
        try:
            cursor.execute(operation,seq)
            res_row = cursor.fetchall()
            return res_row
        except Exception as e:
            raise e
        finally:
            cursor.close()
            if self.conn_pool:
                conn.close()

    def set_paramstyle(self):
        '''设置参数化方式'''
        conn = self.conn_pool.connect() if self.conn_pool else self.conn
        cursor = conn.cursor()
        self.paramstyle = ''
        try:
            module_path = Path(inspect.getmodule(cursor.__class__).__file__)
            for index,name in enumerate(module_path.parts):
                if name == 'site-packages':
                    module_name = module_path.parts[index+1:][0]
                    break
            api = sys.modules[module_name]
            self.paramstyle = api.paramstyle
        except AttributeError:
            api = sys.modules[inspect.getmodule(conn.__class__).__name__]
            self.paramstyle = api.paramstyle
    
    def conn_close(self):
        '''关闭连接池'''
        if self.conn_pool:
            self.conn_pool.dispose()

class table_basic(connect_wrapper,Table):
    '''数据库表类 实现增删改查方法'''
    def __init__(self,conn,table_name='',columns=[],pks=[],up_columns=[],lookup_columns =[],batch_size=50000,fieldmap={},rowmap={},
                 rename={},del_cols = [],char_format = 'upper',default_values = {},strict = True,truncate = False,include_values ={},exclude_values ={},
                 thread_count = 1,paramstyle= '',parallel=False,init_sql = None,after_sql=None,auth_increment={},lookup_operator={},fields_adapter= {},**kwargs):
        '''数据库表类 实现增删改查方法

        Parameters
        ---------------
        conn:PEP249 API connection or return PEP249 API connection function
            原始pep249标准连接 或者为可调用函数 函数返回pep249标准连接
            例1 conn = pymysql.connect(**kwargs)
            例2 conn = lambda :pymysql.connect(**kwargs)
        table_name:str
        数据库表名
        columns:list
            字段名
        pks:list
            Primary key 主键
        up_columns:list
            指定更新的字段
            默认 up_columns = columns
        lookup_columns:list
            指定可以作为查询条件的字段
        batch_size:int
            指定批量提交的行数
        fieldmap:dict
            字段值转换 {fieldname:function}
        rowmap:function
            行处理函数 接受一个dict入参 dict为键值对的行数据 返回一个dict
        del_cols:list
            指定删除的字段
        paramstyle:str
            qmark、numeric、named、format、pyformat
            sql格式化参数的样式 默认 numeric
            参考：https://www.python.org/dev/peps/pep-0249/#paramstyle
        init_sql:str
            初始化执行的sql
        char_format:str
            upper、lower 默认 None
            指定字段名称格式化为大写或者小写
        strict:bool
            默认 True 遇到错误正常报错 
            False 跳过异常数据行 异常记录在 err_rows 属性中
        truncate:bool
            default False 指定是否清空表
        thread_count:int
            实际批量写数据时 使用线程数为 thread_count-1 会保留一个连接作为主连接使用
            所以多线程最小为3 这时会使用2个线程进行批量数据处理
        paramstyle:str
            qmark、numeric、named、format、pyformat
            sql格式化参数的样式 默认 numeric
            参考：https://www.python.org/dev/peps/pep-0249/#paramstyle
        auth_increment:{}
             自增字段 key:字段名称 value:函数对象 默认为None 为None时计算方式为从数据库获取pks[0]字段值 +1
        lookup_operator:dict
        
            指定可以作为查询条件的字段的运算符
            {fieldname1:'=',fieldname1:'like'....}
        '''
        thread_count = 10 if thread_count>10 else thread_count
        Table.__init__(self,table_name = table_name,columns=columns,pks=pks,up_columns=up_columns,lookup_columns=lookup_columns,batch_size=batch_size,fieldmap=fieldmap,rowmap=rowmap,rename=rename,del_cols=del_cols,char_format=char_format,default_values=default_values,strict=strict,truncate=truncate,thread_count=thread_count,parallel=parallel,fields_adapter= fields_adapter,include_values=include_values,exclude_values=exclude_values)
        super().__init__(conn,strict)

        self.auth_increment = auth_increment                                                                                                                                                                                                                                                                

        if paramstyle:
            self.paramstyle = paramstyle
        else:
            self.set_paramstyle()
        self.init_sql = init_sql
        self.lookup_operator = {self.t_char(k):v for k,v in lookup_operator.items()}

        self.sql_insert = self._sql_insert(self.columns_all,self.paramstyle)
        self.sql_update = self._sql_update(self.up_columns,self.pks,self.paramstyle)
        self.sql_lookup = self._sql_lookup(self.columns_all,tuple(set(self.pks+self.lookup_columns)),self.paramstyle)
        self.sql_delete = self._sql_delete(self.pks,self.paramstyle)

        self._current_sql_insert = None
        self._current_sql_update = None
        self._current_sql_lookup = None
        self._current_sql_delete = None

        self.rowcount = 0
        self.after_sql = after_sql

        if self.init_sql:
            self.execute(init_sql)
        
        if self.truncate:
            self._truncate()

        self.auth_increment_current = {}
        if self.auth_increment:
            self.set_auth_increment_current()

    def _paramstyle(self,seq,style ='numeric',numeric_start=0):
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

    @lru_cache(maxsize=100)
    def _sql_insert(self,columns,paramstyle):
        cols = [self.rename.get(n,n) for n in columns]
        sql_insert = "insert into {table} ({cols}) values ({values})".format(table = self.table_name,
                                                                             cols=','.join(cols),
                                                                             values = ','.join(self._paramstyle(cols,paramstyle)))
        return sql_insert

    @lru_cache(maxsize=100)
    def _sql_lookup(self,columns,lookup_atts,paramstyle):
        param_pks = dict(zip(lookup_atts,self._paramstyle(lookup_atts,paramstyle)))
        param_pks = [f"{k} {self.lookup_operator.get(k,'=')} {v}" for k,v in param_pks.items()]
        sql_lookup = "select * from {table} where {where}".format(table = self.table_name,
                                                                  where = ' and '.join(param_pks))
        return sql_lookup

    @lru_cache(maxsize=100)
    def _sql_update(self,up_columns,pks,paramstyle):
        up_columns = [self.rename.get(n,n) for n in up_columns if n not in pks]
        param_up_columns = zip(up_columns,self._paramstyle(up_columns,paramstyle))
        param_pks = dict(zip(pks,self._paramstyle(pks,paramstyle,numeric_start= len(up_columns))))
        param_pks = [f"{k} {self.lookup_operator.get(k,'=')} {v}" for k,v in param_pks.items()]
        param_up_columns = ['='.join(n) for n in param_up_columns]
        
        sql_update = "update {table}  set {values} where {where}".format(table = self.table_name,
                                                                               values =','.join(param_up_columns),
                                                                               where = ' and '.join(param_pks))
        return sql_update

    @lru_cache(maxsize=100)
    def _sql_delete(self,pks,paramstyle):
        param_pks = zip(pks,self._paramstyle(pks,paramstyle))
        param_pks = ['='.join(n) for n in param_pks]
        sql_delete = "delete from {table} where {where}".format(table = self.table_name,
                                                                 where = ' and '.join(param_pks))
        return sql_delete
    
    @lru_cache(maxsize=100)
    def _sql_max_id(self):
        cols = ','.join(['max({}) as {}'.format(id,id) for id in self.pks])
        return  f'select {cols} from {self.table_name}'
        
    def set_auth_increment_current(self):
        # 设置自增id的当前值
        for id,v in self.auth_increment.items():
            if isfunction(v):
                self.auth_increment_current[id] = v
            else:
                res = self.fetchone(self._sql_max_id())
                if res:
                    self.auth_increment_current[id] = res[0]+1
                else:
                    self.auth_increment_current[id] = 1

    def insert(self,row,rename ={}):
        if self.auth_increment:
            # 当存在自增字段时 进行自增计算
            for k,v in self.auth_increment_current.items():
                if isinstance(v,int):
                    row[k] = v+1
                    self.auth_increment_current[k] = v+1
                else:
                    row[k] = v()

        super().insert(row,rename)
        return self.lastrowid

    def delete(self,row,rename={},batch =False):
        super().delete(row,rename)
        if not batch:
            for row in self.batch_delete:
                new_row = [row.get(n) for n in self.pks]
                self.execute(self.sql_delete,new_row)
            self.batch_delete = []

    def lookup(self,row,rename={},fetchone = True,exclude_null = True):
        '''默认使用主键 pks参数作为查询条件 如lookup_columns 参数存在则进行扩展

        Parameters
        -----------
        fetchone:bool
            是否返回单条数据 默认为True
        exclude_null:bool
            是否排除null值 默认为True
        '''
        row = self.pipeline(row,rename)
        lookup_row = tuple(set(chain(self.pks,self.lookup_columns)))
        
        if exclude_null:
            lookup_atts = tuple([n for n in lookup_row if n in row and row[n] is not None])
        else:
            lookup_atts = tuple([n for n in lookup_row if n in row and row[n] is not None])

        new_row = [row[n] for n in lookup_row if n in row and row[n] is not None]
        self.sql_lookup = self._sql_lookup(self.columns_all,lookup_atts,self.paramstyle)
        
        if len(new_row)==len(lookup_atts):
            if fetchone:
                res_row = self.fetchone(self.sql_lookup,new_row)
                log.error('lookupsql: '+ self.sql_lookup + ' args: '+str(new_row))
                if res_row:
                    if not isinstance(res_row,dict):
                        res_row = dict(zip(self.columns_all,res_row))
                    res_row = {self.t_char(k):v for k,v in res_row.items()}
                    return res_row
                else:
                    return {}
            else:
                res_rows = self.fetchall(self.sql_lookup,new_row)
                resdata = []
                for res_row in res_rows:
                    if res_row:
                        if not isinstance(res_row,dict):
                            res_row = dict(zip(self.columns_all,res_row))
                        res_row = {self.t_char(k):v for k,v in res_row.items()}
                        resdata.append(res_row)
                return resdata              
        else:
            raise Exception('参数不匹配:'+str(lookup_atts) +str(new_row))

    def update(self,row,ori_row ={},rename={},batch =False):
        if not ori_row:
            ori_row = self.lookup(row,rename =rename)
        if self.batch_size==1:
            row = self.pipeline(row,rename =rename)
            self.all_row_num+=1
            diff_set = self.diff(row,ori_row)
            
            for n in self.pks:
                diff_set.discard(n)

            if diff_set:
                self.update_row_num +=1
                pks = []
                for pk in self.pks:
                    if row.get(pk,None):
                        pks.append(pk)
                    else:
                        row.pop(pk, None)
                for n in pks:
                    if n in diff_set:
                        diff_set.remove(n)
                self.sql_update = self._sql_update(tuple(diff_set),tuple(pks),self.paramstyle)
                self.sql_update_params = tuple(row[k] for k in diff_set)
                self.sql_update_pks = tuple(row[k] for k in pks)
                self.general_execute(self.sql_update,self.sql_update_params +self.sql_update_pks)
        else:
            row = self.row_diff_reset(row,ori_row)
            super().update(row,ori_row,rename)
        return True

    def standardization(self,row):
        '''pep249 数据格式转换
        '''
        trow = {self.t_char(k):v for k ,v in row.items()}
        new_row = tuple(trow.get(n,None) for n in self.columns_all)

        if self.paramstyle in ('qmark' ,'numeric','format'):
            return new_row
        else:
            return dict(zip(self.columns_all,new_row))

    def load(self):
        if self.batch_insert:
            self.executemany(self.sql_insert,self.batch_insert)
            self.batch_insert = []

        if self.batch_update:
            self.executemany(self.sql_update,self.batch_update)
            self.batch_update = []
 
        if self.batch_delete:
            self.executemany(self.sql_delete,self.batch_delete)
            self.batch_delete = []

    def endload(self):
        self.load()
        # 阻塞等待所有线程执行完毕
        self.parallel_executor.shutdown(wait=True)
        if self.after_sql:
            self.execute(self.after_sql)
        self.conn_close()
        
    def _truncate(self):
        '''执行原生truncate语句
        '''
        self.execute('truncate table '+self.table_name)

class Dimension(table_basic):
    def __init__(self,conn,table_name,lookup_columns,pks,columns=[],cache=True,auth_increment = None,batch_size=1,**kwargs):
        '''维度表
        支持数据库模式的内存缓存和本地缓存 无缝支持sql语句

        Parameters
        -----------
        columns:
            所有字段列表 当insert作为查询条件、lookup时作为返回的字段
        lookup_columns:list
            作为查询条件的字段名称列表 
        cache:bool
            缓存 默认 True 将会缓存整个维度表至本地内存中 后续的操作增删改查会先处理缓存
        auth_increment:dict
            自增主键 传入一个生成主键的函数 默认为None使用数据库主键+1进行计算
        '''
        super().__init__(conn,table_name=table_name,columns=columns,batch_size=batch_size,lookup_columns=lookup_columns,pks=pks,auth_increment=auth_increment,**kwargs)
        self.cache_rows = OrderedDict()
        self.cache = cache
        self.next_id = 0
        if cache:
            src = source_sql(conn,'select * from ({})'.format(self.table_name))
            self.cache_table = Cache_table(src,table_name = self.table_name,columns = self.columns,pks = self.pks,lookup_columns = self.lookup_columns)

    def lookup(self,row,rename={},fetchone = True,exclude_null = True):
        if self.cache:
            res = self.cache_table.lookup(row,rename,fetchone,exclude_null)
            if res:
                return res
        else:
            res = super().lookup(row,rename)
            
        if not res and self.auth_increment:
            self.set_auth_increment_current()
        return res

    def update(self,row,rename={}):
        super().update(row,rename)
        if self.cache:
            self.cache_table.update(row,rename)
        
    def insert(self,row,rename={}):
        super().insert(row,rename={})
        if self.cache:
            self.cache_table.insert(row,rename)
        
    def delete(self,row,rename={}):
        super().delete(row,rename)
        if self.cache:
            super().delete(row,rename)
        
    def clear_cache(self):
        self.cache_table._truncate()
        self.cache_table.endload()
        #self._cache_rows.clear()

class FactTable(table_basic):
    def __init__(self,conn,foreign_key_mapping={},auto_foreign_key=False,**kwargs):
        '''事实表
        Parameters
        -----------
        foreign_key_mapping:{}
            外键映射 {'fk1':[dim,query_mapping,return_field]}
        '''
        super().__init__(conn,**kwargs)
        self.foreign_key_mapping = foreign_key_mapping
        self.auto_foreign_key = auto_foreign_key
        self.foreign_key_null = collections.defaultdict(set())
        
    def transform(self,row):
        '''获取查询外键 保证一致性
        '''
        for fileld,fk in self.foreign_key_mapping.items():
            dim=fk[0]
            res = dim.lookup(row,fk[1])
            if res:
                row[fileld]=res[fk[2]]
            else:
                if self.auto_foreign_key:
                    dim.insert(row)
                    row[fileld] = dim.auth_increment_current[fk[2]]
                else:
                    dim_null_row = {v:row[k] for k,v in fk[1].items()}
                    self.foreign_key_null[dim.table_name].add(dim_null_row)
        return row

            
class ER():
    def __init__(self,tables=[],error = 'skip'):
        self.tables = {table.table_name:table for table in tables}
        self.table_rela = []
        self.error = error

    def add_link(self,fk='',pk='',fieldname_mapping={}):
        '''_summary_

        Parameters
        ----------
        fk : str, optional
            _description_, by default ''
        pk : str, optional
            _description_, by default ''
        fieldname_mapping : dict, optional
            {fk:pk}, by default {}
        '''
        self.table_rela.append((fk,pk,fieldname_mapping))

    def generate(self):
        for n in self.table_rela:
            ftablen_ame,fk = n[0].spilt('.')
            ptable_name,pk = n[1].spilt('.')
            ftable = self.tables[ftablen_ame]
            ptable = self.tables[ptable_name]
            ftable.metadata = {}
            ftable.metadata['foreign_key'] = {fk:[ptable,pk]}
            ftable.metadata['foreign_fieldname_mapping'] = {fk:n[2]}
            ftable.foreign_key_null = collections.defaultdict(set())
            def transform(self,row):
                for fk,mapping_table in self.metadata['foreign_key'].items():
                    dim = mapping_table[0]
                    pk = mapping_table[1]
                    for k,v in self.metadata['foreign_fieldname_mapping'][fk].items():
                        res = dim.lookup({pk:row[fk]}) # 通过外键查询维度表 获取维度表的值 并赋值给事实表 保证一致性
                        if self.error == 'skip':
                            if res:
                                row[k] = res[v]
                            else:
                                dim_null_row = {pk:row[fk]}
                                self.foreign_key_null[dim.table_name].add(dim_null_row)
                        else:
                            raise Exception('{}表中{}外键值{}不存在'.format(dim.table_name,pk,row[fk]))
                return row
            
            # 将方法绑定到实例上
            MethodType(transform,ftable) 

class Change_slowly(Dimension):
    def __init__(self,changedimension=[],changename =[]):
        '''缓慢变化维
        将多个维度的表进行关联 使用一个接口进行统一操作

        Parameters
        -------------
        changedimension:list
            dim_table 维度表类
        changename:list
            [{},{}]
            关联字段名称映射 顺序和changedimension对应
        '''

        self.changedimension = changedimension
        self.changename = changename
        self.slowly_seq = {}

    def lookup(self,row,rename = {}):
        for num in range(len(self.changedimension)):
            dim = self.changedimension[num]
            if num == 0:
                new_row = dim.lookup(row,rename)
            else:
                new_row = dim.lookup(row)
            self.slowly_seq[dim.table_name] = new_row
            if not new_row:
                row = new_row
                break
            if num<=len(self.changename)-1:
                new_row = dim._rename(new_row,self.changename[num])
            row = new_row
        return row

    def insert(self,row,rename ={}):
        for num in range(len(self.changedimension)):
            dim = self.changedimension[num]
            new_row = row
            if num == 0:
                new_row = dim.insert(row,rename)
            else:
                new_row = dim.insert(row)
            dim.load()
            if num<=len(self.changename)-1:
                new_row = dim._rename(new_row,self.changename[num])
            row = new_row

    def update(self,row,rename={}):
        for num in range(len(self.changedimension)):
            dim = self.changedimension[num]
            new_row = row
            if num ==0:
                new_row = dim.update(row,rename)
            else:
                new_row = dim.update(row)
            dim.endload()
            if num<=len(self.changename)-1:
                new_row = dim._rename(new_row,self.changename[num])
            row = new_row
        return row

    def delete(self,row,rename={}):
        for num in range(len(self.changedimension)):
            dim = self.changedimension[num]
            new_row = row
            if num ==0:
                new_row = dim.delete(row,rename)
            else:
                new_row = dim.delete(row)
            dim.endload()
            if num<=len(self.changename)-1 and num>0:
                new_row = dim._rename(new_row,self.changename[num])
            row = new_row
        return row

    def ensure(self,row):
        for num in range(len(self.changedimension)):
            dim = self.changedimension[num]
            new_row = row
            dim.ensure(row)
            dim.load()
            if num<=len(self.changename)-1:
                new_row = dim._rename(new_row,self.changename[num])
            
            row = new_row
        return row

    def endload(self):
        for dim in self.changedimension:
            dim.load()

def Cache_table(data,table_name='',datetime_cols = [],mode =None,inference = True,**kwargs):
    '''将sql数据源转为本地缓存表 使用sqlite实现
    仅支持基础数据类型 str、int、float、datetime
    未指定datetime情况下 将采用自动推测方式确定

    Parameters
    ------------
    data:iterable
        数据源 是一个可迭代对象 每次迭代返回一行数据dict
    datetime_cols:list
        指定datetime列
    mode:str
        指定模式
    inference:bool
        是否自动推测数据类型
    **kwargs:
        其他参数 详见table_basic
    '''
    data_iter = iter(data)
    iters = data_iter
    table_name = table_name if table_name else 'a'+uuid.uuid1().replace('-','')
    if not datetime_cols or inference:
        inference = inference_dtype(data_iter,line_num=10000)
        datetime_cols = inference.datetime
        iters = itertools.chain(inference,data_iter)

    cache_conn = Cache_database(table_name = table_name,columns = data.cols,datetime_cols = datetime_cols,mode =mode)
    cache_table = table_basic(cache_conn,
                            table_name = table_name,
                            batch_size=100000,
                            paramstyle='qmark',
                            **kwargs)

    for row in iters:
        cache_table.insert(row)
    cache_table.load()
    return cache_table

class elastic_basic(Table):
    def __init__(self,conn,index,chunk_size = 2000,batch_size=10000,thread_count = 8,**kwargs):
        '''elasticsearch 数据处理

        Parameters
        ---------------
        conn:Elasticsearch api
            es连接
        index:str
            索引名称
        chunk_size:int
            块大小 default 2000 
        thread_count:int
            线程数 default 8
        '''
        super().__init__(**kwargs)
        self.conn = conn
        self.chunk_size = chunk_size
        self.thread_count = thread_count
        self.batch_size = batch_size
        self.index = self.t_char(index)

    def delete(self,row,rename={},batch =False):
        '''删除数据'''
        super().delete(row,rename)
        
        if batch and '_id' in row:
            row['_op_type'] = 'delete'
            self._batch_append(row,'delete')
        else:
            for row in self.batch_delete:
                new_row = [{'term':{n:row.get(n)}} for n in self.pks if n in row]
                body = {"query":{"bool":{"must":new_row}}}
                self.conn.delete_by_query(index = self.index,body = body)
            self.batch_delete = []

    def lookup(self,row,rename={}):
        '''默认使用主键 pks参数作为查询条件 如lookup_columns 参数存在则进行扩展
        '''
        row = self.row_rename(row,rename)
        row = self.field_transform(row)
        row = self.row_transform(row)
        row = self.transform(row)
        lookup_row = tuple(set(chain(self.pks,self.lookup_columns)))
        lookup_atts  = tuple([n for n in lookup_row if n in row])
        
        new_row = [{'term':{n:row.get(n)}} for n in lookup_row if n in row]
        body = {"query":{"bool":{"must":new_row}}}
        
        res = []
        if len(new_row)==len(lookup_atts):
            log.debug(body)
            res = self.conn.search(body = body,index = self.index)['hits']['hits']
        else:
            raise Exception('参数不匹配:'+str(lookup_atts) +str(new_row))
            
        if res:
            res = res[0]
        if res:
            if isinstance(res,dict):
                res_row = res
            else:
                res_row = dict(zip(self.columns_all,res))
            return res_row
        else:
            None
    
    def standardization(self,row):
        return row 

    def load(self):
        try:
            if self.batch_insert:
                self.executemany(self.batch_insert)
                self.batch_insert = []

            if self.batch_delete:
                self.executemany(self.batch_delete)
                self.batch_delete = []

        except Exception as e:
            raise

    def truncate(self):
        '''清空索引'''
        trunc={"query": {"match_all": {}}}
        self.conn.delete_by_query(index=self.table_name,body=trunc)

    def general_executemany(self,data):
        from elasticsearch.helpers import parallel_bulk
        for success, info in parallel_bulk(client=self.conn, index=self.index, actions=data,chunk_size = self.chunk_size,thread_count = self.thread_count,**self.kwargs):
            if not success:
                self.err_row_num+=1
                self.errs.append(success)
