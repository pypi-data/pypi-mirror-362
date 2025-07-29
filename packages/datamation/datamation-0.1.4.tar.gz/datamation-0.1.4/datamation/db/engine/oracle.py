import sys 
import collections
from dateutil.parser import parse
import cx_Oracle

class oracle():
    def __init__(self,conn):
        self.conn=conn
        self.cursor = conn.cursor()
        self.cons_sql = '''
        select t.CONSTRAINT_NAME,
               t.COLUMN_NAME,
               t1.CONSTRAINT_TYPE,
               t.TABLE_NAME,
               t1.R_OWNER,
               R_CONSTRAINT_NAME
        from all_cons_columns t left join all_constraints t1 on t.CONSTRAINT_NAME = t1.CONSTRAINT_NAME and t.TABLE_NAME = t1.table_name
        where t.TABLE_NAME = :0 AND t1.CONSTRAINT_TYPE = :1
        order by t.CONSTRAINT_NAME
        '''
        self.index_sql ='''
            select 
                   b.index_name,
                   b.column_name,
                   a.table_name,
                   a.uniqueness
            from user_indexes a ,user_ind_columns b
            where a.table_name=b.table_name and a.index_name = b.index_name 
            and a.table_name = :0 AND a.uniqueness = :1
'''
        self.table_sql = '''
            select COLUMN_NAME,
                    DATA_TYPE,
                    DECODE(DATA_PRECISION,NULL ,DATA_LENGTH,DATA_PRECISION) DATA_LENGTH,
                    DATA_SCALE,
                    NULLABLE,
                    DATA_DEFAULT
            from all_tab_columns 
            where table_name =:0
            order by column_id
        '''
        self.table_comments = 'select TABLE_NAME,COMMENTS from user_tab_comments where table_name = :0'
        self.col_comments = 'select COMMENTS,COLUMN_NAME from all_col_comments where table_name = :0'

    def get_explain_plan(conn,sql):
        '''获取sql执行计划

        '''
        sql = 'EXPLAIN PLAN FOR '+ sql
        cur = conn.cursor()
        cur.execute(sql)
        cur.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(format => 'ALL'))")
        plan_str = ''
        for n in cur:
            plan_str+=n
        cur.close()
        return plan_str

    def get_table_pk(conn,table):
        '''获取主键字段
        Parameres
        -----------
        conn:DBAPI
            数据库连接对象
        table:str
            表名
        '''
        sql = f'''select COLUMN_NAME from all_cons_columns  
                   where constraint_name in (select constraint_name from all_constraints where table_name = '{table.upper()}'  and constraint_type ='P')   '''
        cur = conn.cursor()
        cur.execute(sql)
        cons = [n[0] for n in cur.fetchall() if n[0]]
        cur.close()
        return cons

    def get_table_dll(conn,table):
        '''获取表DDL语句 和对应注释
        Parameters
        --------------
        conn: 
            数据库连接
        table: str
            表名
        Returns
        ---------
        str
        '''
        oracle = cx_Oracle

        cur = conn.cursor()

        sql_env = '''
        BEGIN
          DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'STORAGE',FALSE);  --关闭存储熟悉
          DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'TABLESPACE',FALSE); -- 关闭表空间属性
          DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'SEGMENT_ATTRIBUTES', FALSE);  -- 关闭存储属性
          DBMS_METADATA.set_transform_param(DBMS_METADATA.session_transform, 'SQLTERMINATOR', TRUE);  --末尾加分号

          --关闭表索引、外键等关联
          ---DBMS_METADATA.set_transform_param(DBMS_METADATA.session_transform, 'CONSTRAINTS', FALSE);   --约束
          DBMS_METADATA.set_transform_param(DBMS_METADATA.session_transform, 'REF_CONSTRAINTS', FALSE);
          DBMS_METADATA.set_transform_param(DBMS_METADATA.session_transform, 'CONSTRAINTS_AS_ALTER', FALSE);
        END;
        '''

        cur.execute(sql_env)
    
        table = table.upper()
        sql = "select DBMS_METADATA.GET_DDL('TABLE', UPPER('{}'))  from dual ".format(table)
        cur.execute(sql)
        res = cur.fetchall()[0][0]
    
        comment = '''-- 获取表注释sql 
        select case when COMMENTS is not null then 'comment on table '||table_name ||' is \'''|| COMMENTS||\''';'  end COMM_SQL
        from all_tab_comments  
        where table_name = upper('{table}') and COMMENTS is not null
        union all 
        -- 获取字段注释sql 
        select case when COMMENTS is not null then 'comment  on  column '||table_name || '.'|| COLUMN_NAME ||' is \'''|| COMMENTS||\''';'  end COMM_SQL
        from all_col_comments  a 
        where a.TABLE_NAME=upper('{table}') and COMMENTS is not null
        '''.format(table = table)
        cur.execute(comment)
        comments = cur.fetchall()
        comment= ''
        for n in comments:
            comment+='\n'+n[0]
    
        if isinstance(res,oracle.LOB):
            res = res.read().replace('"','')
            res = res.sub('\w*\.','',res)
        
        res = res + '\n'+comment
        res = res.upper()
        cur.close()
        return res

    def get_cons(self,table,cons_type  = 'P'):
        '''获取约束
        '''
        return self.__execute(self.cons_sql,[table,cons_type])
    
    def get_index(self,table,uniqueness = 'NONUNIQUE'):
        '''获取索引
        '''
        return self.__execute(self.index_sql,[table,uniqueness])
    
    def get_tab_description(self,table):
        '''获取字段
        (字段名称、数据类型、数据长度、精度、允许为空、默认值)
        '''
        cols = collections.defaultdict(list)
        self.cursor.execute(self.table_sql.format(table),[table])
        for row in self.cursor:
            cols[row[0]].append(row[0])
            cols[row[0]].append(row[1])
            cols[row[0]].append(row[2])
            cols[row[0]].append(row[3])
            cols[row[0]].append(row[4])
            cols[row[0]].append(row[5])
        return cols
    
    def get_tab_comments(self,table):
        '''表注释
        '''
        comments = {}
        res = self.__execute(self.col_comments,table)
        for n in res:
            comments[n[0]] = [n[1]]
        return comments

    def get_col_comments(self,table):
        '''字段注释
        '''
        comments = {}
        res = self.__execute(self.table_comments,table)
        for n in res:
            comments[n[0]] = [n[1]]
        return comments

    def __execute(self,sql,parameter):
        cons = collections.defaultdict(list)
        self.cursor.execute(sql,parameter)
        for row in self.cursor:
            cons[row[0]].append(row[1])
        return cons

    def get_ctl(self,conn,table,file,skip=0,delimite=',',mode = 'APPEND'):
        type_map = {'DB_TYPE_VARCHAR':'CHAR(1000000000)',
                    'DB_TYPE_DATE':'DATE "YYYY-MM-DD HH24:MI:SS"',
                    'DB_TYPE_CLOB':'CHAR(1000000000)'}
        ctl_info = '''
OPTIONS (skip={skip})
LOAD DATA
INFILE "{file}"
{mode}
INTO table  {table}
FIELDS TERMINATED BY "{delimiter}"
TRAILING NULLCOLS\n
(
        '''.format(skip=skip,file = file,table =table,delimiter =delimite,mode = mode)
        des = self.get_tab_description(conn,table)
        ctl_col = ',\n'.join(['{:20} {}'.format(n[0],type_map.get(n[1].name,'CHAR(1000000000)')) for n in des])
        return ctl_info+ctl_col+'\n)'

    def get_reset_cols(self,table):
        '''
        '''
        oracle = cx_Oracle

        lob_field = []
        default_cols = []
        self.cursor.execute('select * from '+table)
        for col in self.cursor.description:
            if col[1] in [oracle.CLOB,oracle.BLOB]:
                lob_field.append(col[0])
            else:
                default_cols.append(col[0])
        return default_cols + lob_field

class T_oracle(object):
    def __init__(self,conn,table_name,columns=[],up_columns = [],pks=[],batch_size=50000,namemap={},rename={},date_col=[],del_cols = [],**kwargs):
        self.lob_field = []
        self.date_col = date_col

        default_cols = []
        cursor = conn.cursor()

        self.oracle = cx_Oracle

        cursor.execute('select * from '+table_name)
        for col in cursor.description:
            default_cols.append(col[0])
            if col[1] in [self.oracle.DB_TYPE_DATE,self.oracle.DB_TYPE_TIMESTAMP]:
                if col[0] not in self.date_col:
                    self.date_col.append(col[0])
                    
            elif col[1] in [self.orcl.CLOB,self.orcl.BLOB]:
                self.lob_field.append(col[0])
        cursor.close()

        if not columns:
            columns = default_cols

        if pks:
            self.pks = pks
        else:
            self.pks = orcl.get_table_pk(conn,table_name)

        columns = [n for n in columns if not n in self.lob_field] + self.lob_field
        super().__init__(conn,table_name,columns=columns,up_columns=up_columns,pks=self.pks,batch_size=batch_size,namemap=namemap,rename=rename,del_cols = del_cols,**kwargs)
        self.date_col = [self._t_char(n) for n in self.date_col]

    def _transform(self,row):
        for n in self.date_col:
            if n in self.columns and isinstance(row.get(n),str): 
                row[n] = parse(row.get(n)) if row[n] else None
        return row