from dataclasses import dataclass
from collections import namedtuple
from .transform import Tsplitchunk 

class compare_db_data1:
    '''
    适用主键为uuid的表和特大数据量的表 例如指定一个日期字段 将会按日期进行分块进行比对 返回差异数据为日期值列表

    当有多个分区字段时 会逐级进行分块比对 例如指定日期和id字段 将会先按日期分块 比对完成后 将不一致的日期块 再按照id分块 进行比对

    属于非精确差异检测 差异颗粒度为分区字段

    通过继承此类 重写dbms_hash方法 可以使用不同数据库中使用不同的哈希方法

    使用迭代方式比较，以降低数据库压力
    '''
    def __init__(self, source_db, target_db, source_table:str,target_table:str,compare_field:str = 'id',source_field:str = '',target_field:str='',partition_field:str ='id',partition_field_many = [],source_dbms_hash=None,target_dbms_hash=None):
        '''_summary_

        Parameters
        ----------
        source_db : _type_
            _description_
        target_db : _type_
            _description_
        source_table : _type_
            _description_
        target_table : _type_
            _description_
        compare_field : str, optional
            比对字段, by default 'id'
        source_field : str, optional
            源比对字段, by default ''
        target_field : str, optional
            目标比对字段, by default ''
        partition_field : str, optional
            分区字段, by default 'id'
        partition_field_many : list, optional
            多分区字段, by default []
        source_dbms_hash : function, optional
            dbms哈希方法, by default None
        target_dbms_hash : _type_, optional
            dbms哈希方法, by default None
        '''
        self.source_db = source_db
        self.target_db = target_db
        self.source_table = source_table
        self.target_table = target_table
        self.compare_field = compare_field
        self.source_field = source_field if source_field else compare_field
        self.target_field = target_field if target_field else compare_field
        self.partition_many = partition_field_many

        self.partition_field = self.partition_many[0] if self.partition_many else partition_field
        self.partition_many = self.partition_many if self.partition_many else [partition_field]
        self.source_partition = self.get_partition(self.source_db,self.source_table,self.partition_field)
        self.target_partition = self.get_partition(self.target_db,self.target_table,self.partition_field)
        self.partition_diff = []
        self.partition_same = []

        self.source_dbms_hash = source_dbms_hash if source_dbms_hash else self.dbms_hash
        self.target_dbms_hash = target_dbms_hash if target_dbms_hash else self.dbms_hash

    def execute(self,conn,sql,format=''):
        ''' 执行sql语句 
        '''
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        
        cols = [col[0].upper() for col in cur.description]
        cur.close()
        if format =='dict':
            if data:
                return [dict(zip(cols,n)) for n in data]
        else:
            if len(data) ==1 and not data[0][0]:
                return []
            else:
                return [n[0] for n in data]
        
    def get_partition(self,conn,table_name,partition_field,where=''):
        '''获取表的分区信息 返回一个分区值列表'''
        sql = f'select distinct {partition_field} from {table_name}'
        if where:
            sql += f' where {where}'
        return self.execute(conn,sql)

    def init_partition_detection(self):
        '''获取分区差异'''
        for n in set( self.source_partition ).difference(set( self.target_partition )):
            self.partition_diff.append(n)
        for n in set( self.source_partition ).intersection(set( self.target_partition )):
            self.partition_same.append(n)

    def dbms_hash(self,field):
        '''获取数据库的hash方法'''
        return f'md5(concat({field}))'
     
    def get_diff_sql(self,source=True,format='list',query_field='*',many=True):
        if source:
            replace_field = self.source_dbms_hash(self.source_field) 
            sqls = [self.get_source_sql(n).replace(replace_field,query_field) for n in self.partition_diff]
        else:
            replace_field = self.target_dbms_hash(self.target_field) 
            sqls = [self.get_target_sql(n).replace(replace_field,query_field) for n in self.partition_diff]
        
        if format=='list':
            return sqls
        
        elif format=='str':
            if many:
                return ';\n'.join(sqls)
            else:
                if sqls:
                    wheres = ' or '.join([n.spilt('where')[1] for n in sqls])
                    return sqls[0].spilt('where')[0] + ' where ' + wheres
                else:
                    return ''
    
    def get_source_sql(self,partition):
        '''获取分区sql'''
        sql = 'select {hash} from {table_name} where {partition_field} = {partition_value}'
        sql = sql.format(hash = self.source_dbms_hash(self.source_field),table_name = self.source_table,partition_field = self.partition_field,partition_value = partition)
        return sql
    
    def get_target_sql(self,partition):
        '''获取分区sql'''
        sql = 'select {hash} from {table_name} where {partition_field} = {partition_value}'
        sql = sql.format(hash = self.target_dbms_hash(self.target_field),table_name = self.target_table,partition_field = self.partition_field,partition_value = partition)
        return sql

    def record_partition_diff(self,value):
        '''记录差异
        '''
        self.partition_diff.append(value)
    
    def stop(self):
        '''检测结束条件 当全部分区值都经过比对后结束'''
        if not self.partition_same:
            return True 
        
    def compare_partition(self):
        '''获取分区数据 循环迭代计算'''
        while 1:
            if self.stop():
                break

            for partition in self.partition_many:
                # 当有多个分区时，进行迭代比较
                if self.partition_field != partition:
                    self.partition_field = partition
                    if self.partition_diff:
                        wheres = ' or '.join([n[1] for n in self.get_diff_sql(source=True)])
                    self.source_partition = self.get_partition(self.source_db,self.source_table,self.partition_field,wheres)
                    self.target_partition = self.get_partition(self.target_db,self.target_table,self.partition_field,wheres)
                    self.partition_diff = []
                    self.partition_same = []
                    self.init_partition_detection()

                for num,item in enumerate(self.partition_same):
                    
                    self.partition_same.remove(item)
                    source_sql = self.get_source_sql(item)
                    data1 = self.execute(self.source_db,source_sql)
                    target_sql = self.get_target_sql(item)
                    data2 = self.execute(self.target_db,target_sql)

                    if data1 != data2:
                        if not item in self.partition_diff:
                            self.record_partition_diff(item)
                
    def get_diff_rowcount(self):
        sqls = self.get_diff_sql(query_field='count(1)')
        rowcount = 0
        for sql in sqls:
            res = self.execute(self.source_db,sql)
            if res:
                rowcount +=res[0]
        self.rowcount = rowcount

    def compare_partition_batch(self):
        '''获取分区数据 一次性计算'''
        for n in self.partition_same:
            source_sql += 'union all' +self.get_source_sql(n)
            target_sql += 'union all' +self.get_target_sql(n)

        data1 = self.execute(self.source_db,source_sql)
        data2 = self.execute(self.target_db,target_sql)

        for num,item in enumerate(self.partition_same):
            if data1[num] != data2[num]:
                if item not in self.partition_diff:
                    self.partition_diff.append(item)

    def generate_dml_sql(self):
        source_sql = self.get_diff_sql()
        target_sql = self.get_diff_sql(False)

        diff_rows ={'update':[],'insert':[]}
        for num ,item in enumerate(self.partition_diff):
            diff_cols = []
            data1 = self.execute(self.source_db,source_sql[num],format='dict')
            data2 = self.execute(self.target_db,target_sql[num],format='dict')

            data1 = data1[0] if data1 else {}
            data2 = data2[0] if data2 else {}

            if data2:
                for k in data1.keys():
                    if data1[k]!=data2[k]:
                        diff_cols.append(k)
                update_sql =','.join(diff_cols)
                upsql = source_sql[num].replace('*',update_sql)
                diff_rows['update'].append(upsql)
            else:
                diff_rows['insert'].append(source_sql[num])
        self.diff_dml = diff_rows

class compare_db_data2(compare_db_data1):
    '''适用于主键为自增长的表 通过二分法进行分块比较提高效率
    '''
    def get_partition(self,conn,table_name,partition_field):
        '''获取表的最大值 拆分为不同区间'''
        sql = f'select max({partition_field})+1 from {table_name}'
        maxid = self.execute(conn,sql)[0]
        return list(Tsplitchunk(start = 0 ,end = maxid,num_blocks=2))
    
    def init_partition_detection(self):
        '''获取分区差异 通过主键进行二分计算分区时 会出现分区值不一致的情况 以源表分区为比对标准'''
        for n in self.source_partition:
            self.partition_same.append(n)

    def record_partition_diff(self,value):
        '''记录差异
        '''
        if (value[1] - value[0])>1:
            spilt_partition = list(Tsplitchunk(start = value[0] ,end = value[1],num_blocks=2))
            self.partition_same.extend(spilt_partition)
        
        elif (value[1] - value[0])==1:
            self.partition_diff.append(value)

    def stop(self):
        '''检测结束条件 当全部分区值都经过比对后结束'''
        seq = [n[1]-n[0] for n in self.partition_same]
        return len(self.partition_same) == sum(seq)

    def get_source_sql(self,partition):
        '''获取分区sql'''
        sql = 'select {hash} from {table_name} where {partition_field} >= {partition_value_start} and {partition_field} <{partition_value_end}'
        sql = sql.format(hash = self.source_dbms_hash(self.source_field),
                         table_name = self.source_table,
                         partition_field = self.partition_field,
                         partition_value_start = partition[0],
                         partition_value_end = partition[1],
                         )
        return sql
    
    def get_target_sql(self,partition):
        '''获取分区sql'''
        sql = 'select {hash} from {table_name} where {partition_field} >= {partition_value_start} and {partition_field}<{partition_value_end}'
        sql = sql.format(hash = self.target_dbms_hash(self.target_field),
                         table_name = self.target_table,
                         partition_field = self.partition_field,
                         partition_value_start = partition[0],
                         partition_value_end = partition[1],
                         )
        return sql
    
def get_sqldata_diff1(source_db,target_db,source_table:str,target_table:str,compare_field: str = 'id',source_field: str = '',target_field: str = '',partition_field: str = 'id',partition_field_many: list = [],source_dbms_hash=None,target_dbms_hash=None):
    '''适用主键为uuid的表 例如指定一个日期字段 将会按日期进行分块进行比对 返回差异数据为日期值列表

    当有多个分区字段时 会逐级进行分块比对 传入时顺序为从左到右 粗粒度到细粒度的不同分组级别 例如指定日期和id字段 将会先按日期分块 比对完成后 将不一致的日期块 再按照id分块 进行比对

    属于非精确比对 颗粒度为所指定分区字段的值

    返回的差异列表id对应为数据源的值

    此方法便捷封装函数 如需要更多自定义功能 请使用compare_db_data1类

    Parameters
    -----------
    source_db : connection
        数据源
    target_db : connection
        目标库
    source_table : str
        数据源表名
    target_table : str
        目标表名
    compare_field : str
        比对字段, 默认 'id'
    source_field : str
        数据源字段, 默认''
    target_field : str
        目标字段, 默认''
    partition_field : str
        分区字段, 默认 'id'
    partition_field_many : list
        多分区字段, 默认 []
    source_dbms_hash : function
        数据源hash函数, 默认
    target_dbms_hash : function
        目标库hash函数, ，默认 None
    '''
    diff = compare_db_data1(source_db=source_db,target_db=target_db,source_table=source_table,target_table=target_table,compare_field=compare_field,source_field=source_field,target_field=target_field,partition_field=partition_field,partition_field_many=partition_field_many,source_dbms_hash=source_dbms_hash,target_dbms_hash=target_dbms_hash)
    # 初始化分区差异
    diff.init_partition_detection()
    # 比对
    diff.compare_partition()

    Diff_result = namedtuple("Diff",["sql", "result"])
    Diff_result.sql = diff.diff_dml
    Diff_result.result = [n[0] for n in diff.partition_diff]
    return Diff_result

    #return diff.partition_diff

def get_sqldata_diff2(source_db,target_db,source_table:str,target_table:str,compare_field: str = 'id',source_field: str = '',target_field: str = '',partition_field: str = 'id',partition_field_many: list = [],source_dbms_hash = None,target_dbms_hash = None):
    '''当主键id为自增数值类型时 使用二分法进行计算分块比对

    此方法便捷封装函数 如需要更多自定义功能 请使用compare_db_data2类

    Parameters
    ----------
    source_db : _type_
        源数据库连接
    target_db : _type_
        目标数据库连接
    source_table : str
        源表
    target_table : str
        目标表
    compare_field : str, optional
        比对字段, by default 'id'
    source_field : str, optional
        比对字段, by default compare_field
    target_field : str, optional
        目标比对字段, by default compare_field
    partition_field : str, optional
        分区字段, by default 'id'
    partition_field_many : list, optional
        多分区字段, by default []
    source_dbms_hash : Callable[[str], str], optional
        dbms哈希方法, by default None
    target_dbms_hash : Callable[[str], str], optional
        dbms哈希方法, by default None

    Returns
    -------
    list
        差异列表
    '''
    diff = compare_db_data2(source_db=source_db,target_db=target_db,source_table=source_table,target_table=target_table,compare_field=compare_field,source_field=source_field,target_field=target_field,partition_field=partition_field,partition_field_many=partition_field_many,source_dbms_hash=source_dbms_hash,target_dbms_hash=target_dbms_hash)
    # 初始化分区差异
    diff.init_partition_detection()
    # 比对
    diff.compare_partition()

    diff.generate_dml_sql()

    Diff_result = namedtuple("Diff",["sql", "result"])
    Diff_result.sql = diff.diff_dml
    Diff_result.result = [n[0] for n in diff.partition_diff]
    return Diff_result
    #return [n[0] for n in diff.partition_diff]

def dbms_hash_mysql(field):
    '''mysql数据库的hash方法'''
    return f'sum(substring(hex(CONVERT(MD5(CONCAT({field})),BINARY)),56,8))'

def dbms_hash_pgsql(field):
    '''pgsql数据库的hash方法'''
    return f"sum(SUBSTRING(encode(md5(concat({field}))::bytea,'hex'),56,8)::numeric)"

def dbms_hash_count(field):
    '''统计数量'''
    return f"count(1)"
