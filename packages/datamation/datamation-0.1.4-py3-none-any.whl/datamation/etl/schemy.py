from datetime import datetime

from sqlalchemy import Table,Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean, BigInteger, Float, Date, Time, LargeBinary, SmallInteger, UniqueConstraint ,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datamation.db import sqlalchemy_engine,sqlsync

Base = declarative_base()

class etl_dictionary(Base):
    __tablename__ = 'etl_dictionary'
    __table_args__ = (
        UniqueConstraint('category', 'item', name='unique_category_item'),
        {'comment': '字典表'}
    )
    id = Column(Integer, primary_key=True,comment='主键',autoincrement=True)
    category = Column(String(100), nullable=False,comment='类别')
    item = Column(String(100), nullable=False,comment='项目')
    value = Column(String(100), nullable=False,comment='值')
    comments = Column(String(100), nullable=False,comment='说明')
    create_date = Column(DateTime, nullable=False,comment='创建时间',default=datetime.now)

class etl_sources(Base):
    __tablename__ = 'etl_sources'
    __table_args__ = (
        UniqueConstraint('source_name', name='unique_source_name'),
        {'comment': '数据源表'}
    )
    id = Column(Integer, primary_key=True,comment='主键',autoincrement=True)
    source_name = Column(String(100), nullable=False,comment='数据源名称')
    category = Column(String(100), nullable=False,comment='数据源类型')
    connect_args = Column(JSON, nullable=False,comment='连接参数')
    comments = Column(String(100), nullable=False,comment='说明')
    create_date = Column(DateTime, nullable=False,comment='创建时间',default=datetime.now)

class etl_task_info(Base):
    __tablename__ = 'etl_task_info'
    __table_args__ = (
        UniqueConstraint('task_group', 'source_table', 'target_table', name='unique_task_group'),
        {'comment': '任务表'}
    )
    id = Column(Integer, primary_key=True,comment='主键',autoincrement=True)
    task_group = Column(String(100), nullable=False,comment='任务组')
    comments = Column(String(100), nullable=False,comment='表说明或者任务说明')
    source = Column(Integer, nullable=False,comment='源数据源id')
    source_table = Column(String(30), nullable=False,comment='源表')
    target = Column(Integer, ForeignKey('etl_sources.id'), nullable=False,comment='目标数据源id')
    target_table = Column(String(30), nullable=False,comment='目标表')
    is_increment = Column(Integer, nullable=False,comment='1 增量 0 全量',default=0)
    delete_factor = Column(String(1000), nullable=True,comment='删除条件')
    query_factor = Column(String(1000), nullable=True,comment='查询条件')
    delete_cusfactor = Column(String(1000), nullable=True,comment='自定义删除条件')
    status = Column(Integer, nullable=False,comment='状态 （1 启用 0 停用）')
    run_status = Column(Integer, nullable=False,comment='运行状态')
    before_sql = Column(String(2000), nullable=True,comment='同步前执行sql')
    affter_sql = Column(String(2000), nullable=True,comment='同步后执行sql')
    pks = Column(String(100), nullable=False,comment='主键')
    fieldsmap = Column(JSON, nullable=False,comment='字段映射')
    script = Column(JSON, nullable=False,comment='脚本')
    create_date = Column(DateTime, nullable=False,comment='创建时间',default=datetime.now)

class etl_task_log(Base):
    __tablename__ = 'etl_task_log'
    __table_args__ = (
        {'comment': '任务日志表'}
    )
    id = Column(Integer, primary_key=True,comment='主键',autoincrement=True)
    task = Column(Integer, nullable=False,comment='任务id')
    log_text = Column(Text, nullable=False,comment='执行日志')
    log_file = Column(String(200), nullable=True,comment='日志文件')
    status = Column(Integer, nullable=False,comment='状态 （1 成功 0 失败）')
    start_time = Column(DateTime, nullable=False,comment='任务开始时间')
    end_time = Column(DateTime, nullable=False,comment='任务结束时间')
    create_date = Column(DateTime, nullable=False,comment='创建时间',default=datetime.now)

class etl_task_files(Base):
    __tablename__ = 'etl_task_files'
    __table_args__ = (
        {'comment': '任务文件表'}
    )
    id = Column(Integer, primary_key=True,comment='主键',autoincrement=True)
    task = Column(Integer,nullable=False,comment='任务id')
    pathname = Column(String(200), nullable=False,comment='文件路径')
    filename = Column(String(200), nullable=False,comment='文件名')
    size = Column(Integer, nullable=False,comment='文件大小')
    create_date = Column(DateTime, nullable=False,comment='创建时间',default=datetime.now)

class TestSource(Base):
    __tablename__ = 'etl_test_source'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    created_date = Column(DateTime,default=datetime.now)

class TestTarget(Base):
    __tablename__ = 'etl_test_target'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    created_date = Column(DateTime,default=datetime.now)

# 初始化数据库表
def InitDb(conn):
    '''在数据库中创建etl配置表'''
    engine = sqlalchemy_engine(conn)

    # 创建表结构
    print('创建表结构...')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    print('表结构创建完成')

    # 向表中插入模拟数据
    print('初始化表数据...')
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([
        etl_dictionary(category='datasource', item='mysql', value='1', comments='启用'),
        etl_dictionary(category='datasource', item='oracle', value='1', comments='启用'),
        etl_dictionary(category='datasource', item='oss-aliyun', value='1', comments='启用'),
        etl_dictionary(category='datasource', item='xlsx', value='1', comments='启用'),
        etl_dictionary(category='datasource', item='csv', value='1', comments='启用'),
        
        etl_sources(source_name='mysql_test_source1', category='mysql', connect_args={'host': '127.0.0.1', 'port': 3306, 'database': 'test_data', 'user': 'root', 'passwd': ''}, comments='MySQL test数据源1'),
        etl_sources(source_name='mysql_test_source2', category='mysql', connect_args={'host': '127.0.0.1', 'port': 3306, 'database': 'test_data', 'user': 'root', 'passwd': ''}, comments='MySQL test数据源2'),
        
        etl_task_info(task_group='test_group', comments='测试任务', source=1, source_table='etl_test_source', target=1, target_table='etl_test_target', is_increment=0, delete_factor=None, query_factor=None, delete_cusfactor=None, status=1, run_status=0, before_sql=None, affter_sql=None, pks='id', fieldsmap={}, script={}, create_date=datetime.now()),
        
        TestSource(name='Source 1', description='Description of source 1'),
        TestSource(name='Source 2', description='Description of source 2')
        
        ])

    session.commit()
    # 关闭数据库连接
    session.close()
    print('初始化完成')


class DatabaseManager:
    def __init__(self, conn):
        self.engine = sqlalchemy_engine(conn)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

class DictionaryService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_entry(self, category, item, value, comments):
        with self.db_manager.get_session() as session:
            new_entry = etl_dictionary(
                category=category,
                item=item,
                value=value,
                comments=comments,
                create_date=datetime.now()
            )
            session.add(new_entry)
            session.commit()

    def get_entries_by_category(self, category):
        with self.db_manager.get_session() as session:
            return session.query(etl_dictionary).filter_by(category=category).all()

    def update_entry(self, id, **kwargs):
        with self.db_manager.get_session() as session:
            entry = session.query(etl_dictionary).filter_by(id=id).first()
            if entry:
                for key, value in kwargs.items():
                    setattr(entry, key, value)
                session.commit()

    def delete_entry(self, id):
        with self.db_manager.get_session() as session:
            entry = session.query(etl_dictionary).filter_by(id=id).first()
            if entry:
                session.delete(entry)
                session.commit()

class SourceService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_source(self, source_name, category, connect_args, comments):
        with self.db_manager.get_session() as session:
            new_source = etl_sources(
                source_name=source_name,
                category=category,
                connect_args=connect_args,
                comments=comments,
                create_date=datetime.now()
            )
            session.add(new_source)
            session.commit()

    def get_source_by_id(self, id):
        with self.db_manager.get_session() as session:
            return session.query(etl_sources).filter_by(id=id).first()
        
    def get_source_by_name(self, source_name, category):
        with self.db_manager.get_session() as session:
            return session.query(etl_sources).filter_by(source_name=source_name,category =category).first()
    
    def query_sources(self):
        with self.db_manager.get_session() as session:
            return session.query(etl_sources).all()
        
    def update_source(self, id, **kwargs):
        with self.db_manager.get_session() as session:
            source = session.query(etl_sources).filter_by(id=id).first()
            if source:
                for key, value in kwargs.items():
                    setattr(source, key, value)
                session.commit()

    def delete_source(self, id):
        with self.db_manager.get_session() as session:
            source = session.query(etl_sources).filter_by(id=id).first()
            if source:
                session.delete(source)
                session.commit()

class TaskService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_task(self, task_group, comments, source, source_table, target, target_table, is_increment, delete_factor, query_factor, delete_cusfactor, status, run_status, before_sql, affter_sql, pks, fieldsmap, script):
        with self.db_manager.get_session() as session:
            new_task = etl_task_info(
                task_group=task_group,
                comments=comments,
                source=source,
                source_table=source_table,
                target=target,
                target_table=target_table,
                is_increment=is_increment,
                delete_factor=delete_factor,
                query_factor=query_factor,
                delete_cusfactor=delete_cusfactor,
                status=status,
                run_status=run_status,
                before_sql=before_sql,
                affter_sql=affter_sql,
                pks=pks,
                fieldsmap=fieldsmap,
                script=script,
                create_date=datetime.now()
            )
            session.add(new_task)
            session.commit()

    def get_task_by_id(self, id):
        with self.db_manager.get_session() as session:
            return session.query(etl_task_info).filter_by(id=id).first()

    def update_task(self, id, **kwargs):
        with self.db_manager.get_session() as session:
            task = session.query(etl_task_info).filter_by(id=id).first()
            if task:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                session.commit()

    def delete_task(self, id):
        with self.db_manager.get_session() as session:
            task = session.query(etl_task_info).filter_by(id=id).first()
            if task:
                session.delete(task)
                session.commit()

class ETLTaskRunner:
    def __init__(self,conn,driver:dict):
        ''' ETL任务执行器

        Parameters
        ----------
        conn : 可调用数据库连接对象
            例 lambda: pymysql.connect(host='localhost', user='user', password='password', database='mydatabase')
        driver : dict
            驱动对象字典 例
            {
                'mysql': pymysql,
                'postgres': psycopg2
            }
        '''
        self.db_manager = DatabaseManager(conn)
        self.sqlsync = sqlsync
        self.driver = driver

    def run_sync_tasks(self):
        with self.db_manager.get_session() as session:
            # 获取启用且未运行的任务
            tasks = session.query(etl_task_info).filter_by(status=1, run_status=0).all()
            print('待执行任务数:',len(tasks))
            for index,task in enumerate(tasks):
                try:
                    # 获取源和目标数据源信息
                    source = session.query(etl_sources).filter_by(id=task.source).first()
                    target = session.query(etl_sources).filter_by(id=task.target).first()

                    if not source or not target:
                        print(f"任务{index} {task.id} 缺少源或目标数据源信息，跳过。")
                        continue

                    # 更新任务状态为正在运行
                    task.run_status = 1
                    session.commit()

                    truncate = not bool(task.is_increment)

                    # 打印日志
                    print(f"任务{index} {task.source_table} -> {task.target_table} 启动运行...")

                    # 调用 sqlsync 执行同步
                    self.sqlsync(
                        source_conn = lambda:self.driver[source.category].connect(**source.connect_args),
                        source_table = task.source_table,
                        target_conn = lambda:self.driver[target.category].connect(**target.connect_args),
                        target_table = task.target_table,
                        before_sql = task.before_sql,
                        after_sql = task.affter_sql,
                        truncate = truncate,
                        rename = task.fieldsmap,
                        rich=False
                        
                    )
                    print(f"任务{index} {task.source_table} -> {task.target_table} 同步完成")

                    # 同步成功，更新任务状态
                    task.run_status = 0
                    log_status = 1
                    log_text = "同步成功"
                except Exception as e:
                    # 处理同步异常
                    log_text = f"任务{task.id} {task.source_table} -> {task.target_table} 同步失败: {e}"
                    task.run_status = 0
                    log_status = 0
                    print(log_text)

                finally:
                    # 记录任务日志
                    task_log = etl_task_log(
                        task=task.id,
                        log_text=log_text,
                        status=log_status,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        create_date=datetime.now()
                    )
                    session.add(task_log)
                    session.commit()

if __name__ == '__main__':
    import pymysql
    conn = lambda:pymysql.connect(host='127.0.0.1',user='root',passwd='',port=3306,database='test_data')
    InitDb(conn)
    etl = ETLTaskRunner(conn,{'mysql':pymysql})
    etl.run_sync_tasks()
    