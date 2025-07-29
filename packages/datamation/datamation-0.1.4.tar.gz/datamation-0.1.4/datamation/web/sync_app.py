import os
import sys
from typing import Dict, Any, Optional

import pymysql
import psycopg2

import datamation as dm
from datamation.db.utils.general import dbcfg
from datamation.utils import zip_files
from datamation.db.extend import pg_dump,pgtable

import streamlit as st

# 数据库类型配置
DB_TYPES = {
    'postgresql': {
        'name': 'PostgreSQL',
        'default_port': 5432,
        'driver': psycopg2
    },
    'mysql': {
        'name': 'MySQL',
        'default_port': 3306,
        'driver': pymysql
    }
}

def init_connection_config():
    """初始化数据库连接配置"""
    if 'db_configs' not in st.session_state:
        try:
            st.session_state.db_configs = dbcfg()
        except:
            st.session_state.db_configs = None
            
    if 'source_config' not in st.session_state:
        st.session_state.source_config = {
            'type': 'postgresql',
            'host': '',
            'port': DB_TYPES['postgresql']['default_port'],
            'user': '',
            'password': '',
            'database': '',
            'schema': 'public'
        }
    if 'target_config' not in st.session_state:
        st.session_state.target_config = {
            'type': 'postgresql',
            'host': '',
            'port': DB_TYPES['postgresql']['default_port'],
            'user': '',
            'password': '',
            'database': '',
            'schema': 'public'
        }

def create_connection(config: Dict[str, Any]) -> Optional[callable]:
    """创建数据库连接"""
    try:
        db_type = config['type']
        driver = DB_TYPES[db_type]['driver']
        
        if db_type == 'mysql':
            return lambda: driver.connect(
                host=config['host'],
                port=int(config['port']),
                user=config['user'],
                password=config['password'],
                database=config['database'],
                write_timeout=50000,
                connect_timeout=20000
            )
        elif db_type == 'postgresql':
            connect_args = {
                'host': config['host'],
                'port': int(config['port']),
                'user': config['user'],
                'password': config['password'],
                'dbname': config['database']
            }
            
            # 如果配置中包含options，则添加到连接参数中
            if 'options' in config:
                connect_args['options'] = config['options']
            # 如果配置中包含schema但没有options，则通过options设置search_path
            elif 'schema' in config and config['schema']:
                connect_args['options'] = f"-c search_path={config['schema']}"
                
            conn = driver.connect(**connect_args)
            return lambda: conn
    except Exception as e:
        st.error(f'数据库连接失败: {str(e)}')
        return None

def test_connection(config: Dict[str, Any]) -> bool:
    """测试数据库连接"""
    try:
        conn_factory = create_connection(config)
        if conn_factory:
            conn = conn_factory()
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1')
            conn.close()
            return True
        return False
    except Exception as e:
        return False

def render_db_config(prefix: str, config: Dict[str, Any]):
    """渲染数据库配置表单"""
    with st.expander('{}数据库配置'.format('源' if prefix == 'source' else '目标'), expanded=True):
        # 添加配置选择下拉框
        if st.session_state.db_configs:
            saved_configs = [''] + list(st.session_state.db_configs.keys())
            selected_config = st.selectbox(
                '选择已保存配置',
                options=saved_configs,
                key=f'{prefix}_saved_config'
            )
            
            if selected_config and selected_config != '':
                cfg = st.session_state.db_configs[selected_config]
                config.update({
                    'host': cfg.get('host', ''),
                    'port': int(cfg.get('port', DB_TYPES[config['type']]['default_port'])),
                    'user': cfg.get('user', ''),
                    'password': cfg.get('password', ''),
                    'database': cfg.get('dbname', '')
                })
        
        col1, col2 = st.columns(2)
        with col1:
            db_type = st.selectbox(
                '数据库类型',
                options=list(DB_TYPES.keys()),
                format_func=lambda x: DB_TYPES[x]['name'],
                key=f'{prefix}_type',
                index=list(DB_TYPES.keys()).index(config['type'])
            )
            
            # 更新数据库类型和默认端口
            if config['type'] != db_type:
                config['type'] = db_type
                config['port'] = DB_TYPES[db_type]['default_port']
            
            config['host'] = st.text_input('主机地址', config['host'], key=f'{prefix}_host')
            config['port'] = st.number_input('端口', value=config['port'], key=f'{prefix}_port')
            config['database'] = st.text_input('数据库名', config['database'], key=f'{prefix}_database')
            if config['type'] == 'postgresql':
                config['schema'] = st.text_input('Schema', config.get('schema', 'public'), key=f'{prefix}_schema')
        with col2:
            config['user'] = st.text_input('用户名', config['user'], key=f'{prefix}_user')
            config['password'] = st.text_input('密码', config['password'], key=f'{prefix}_password', type='password')
            
            # 添加测试连接按钮
            if st.button('测试连接', key=f'{prefix}_test_connection'):
                with st.spinner('正在测试连接...'):
                    if test_connection(config):
                        st.success('连接成功！')
                    else:
                        st.error('连接失败，请检查配置是否正确')

def sync_data():
    """数据同步页面"""
    st.title('数据同步')
    
    # 数据库配置
    col1, col2 = st.columns(2)
    with col1:
        render_db_config('source', st.session_state.source_config)
    with col2:
        render_db_config('target', st.session_state.target_config)
    
    # 同步配置
    col1, col2 = st.columns(2)
    with col1:
        src_table = st.text_input('源表名')
    with col2:
        tag_table = st.text_input('目标表名')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        batch_size = st.number_input('批量大小', min_value=1000, value=20000, step=1000)
    with col2:
        truncate = st.checkbox('同步前清空目标表', value=True)
    
    # 执行同步
    if st.button('开始同步', type='primary'):
        if not (src_table and tag_table):
            st.error('请输入源表名和目标表名')
            return
            
        source_conn = create_connection(st.session_state.source_config)
        target_conn = create_connection(st.session_state.target_config)
        
        if source_conn and target_conn:
            try:
                # 创建一个占位容器用于显示同步进度
                status_container = st.empty()
                def progress_callback(message):
                    status_container.info(message)
                
                with st.spinner('正在同步数据...'):
                    # 创建一个可滚动的容器
                    output_container = st.container()
                    with output_container:
                        # 重定向print输出到StringIO
                        import sys
                        from io import StringIO
                        old_stdout = sys.stdout
                        sys.stdout = output = StringIO()
                        try:
                            dm.sqlsync(
                                source_conn=source_conn,
                                src_table=src_table,
                                target_conn=target_conn,
                                tag_table=tag_table,
                                batch_size=batch_size,
                                truncate=truncate,
                                rich=False,  # 禁用rich进度条，使用普通输出
                                table_cls= pgtable if st.session_state.target_config['type'] == 'postgresql' else dm.table_basic,
                            )
                        finally:
                            # 恢复标准输出
                            sys.stdout = old_stdout
                            # 在可滚动容器中显示同步过程的输出
                            st.text_area("同步过程", value=output.getvalue(), height=300)
                
                st.success('数据同步完成！')
            except Exception as e:
                st.error(f'同步失败: {str(e)}')

def compare_data():
    """数据比对页面"""
    st.title('数据比对')
    
    # 数据库配置
    col1, col2 = st.columns(2)
    with col1:
        render_db_config('source', st.session_state.source_config)
    with col2:
        render_db_config('target', st.session_state.target_config)
    
    col1, col2 = st.columns(2)
    with col1:
        src_table = st.text_input('源表名')
    with col2:
        tag_table = st.text_input('目标表名')
    
    if st.button('开始比对', type='primary'):
        if not (src_table and tag_table):
            st.error('请输入源表名和目标表名')
            return
            
        source_conn = create_connection(st.session_state.source_config)
        target_conn = create_connection(st.session_state.target_config)
        
        if source_conn and target_conn:
            try:
                with st.spinner('正在比对数据...'):
                    # 创建可滚动容器
                    with st.container():
                        
                        # 数据内容比对
                        st.write('数据内容差异：')
                        comp = dm.get_sqldata_diff2(
                            source_conn(), 
                            target_conn(), 
                            src_table, 
                            tag_table,
                            compare_field='id'
                        )
                        if comp:
                            st.text_area("差异详情", value=str(comp), height=300)
                        else:
                            st.info('数据内容一致')
            except Exception as e:
                st.error(f'比对失败: {str(e)}')

def compare_structure():
    """数据结构比对页面"""
    st.title('数据结构比对')
    
    # 数据库配置
    col1, col2 = st.columns(2)
    with col1:
        render_db_config('source', st.session_state.source_config)
    with col2:
        render_db_config('target', st.session_state.target_config)
    
    if st.button('开始比对', type='primary'):
        source_conn = create_connection(st.session_state.source_config)
        target_conn = create_connection(st.session_state.target_config)
        
        if source_conn and target_conn:
            try:
                with st.spinner('正在比对数据结构...'):
                    # 创建可滚动容器
                    with st.container(border=False,height=700):
                        diff_sql = dm.get_sqldb_diff(
                            source_conn(), 
                            target_conn(), 
                            st.session_state.target_config['type'],
                        )
                        if diff_sql:
                            st.write('表结构差异：')
                            # 将所有SQL语句合并成一个字符串
                            all_sql = '\n'.join(diff_sql)
                            st.code(all_sql)
                        else:
                            st.success('表结构完全一致')
            except Exception as e:
                st.error(f'比对失败: {str(e)}',)
                raise e
                
def backup_data():
    """数据备份页面"""
    st.title('数据备份')
    
    # 数据库配置
    st.subheader('数据库配置')
    db_config = {}
    
    # 添加配置选择下拉框
    if st.session_state.db_configs:
        saved_configs = [''] + list(st.session_state.db_configs.keys())
        selected_config = st.selectbox(
            '选择已保存配置',
            options=saved_configs,
            key='backup_saved_config'
        )
        
        if selected_config and selected_config != '':
            cfg = st.session_state.db_configs[selected_config]
            db_config.update({
                'type': 'postgresql' if 'type' not in cfg else cfg['type'],
                'host': cfg.get('host', ''),
                'port': int(cfg.get('port', DB_TYPES['postgresql']['default_port'])),
                'user': cfg.get('user', ''),
                'password': cfg.get('password', ''),
                'database': cfg.get('dbname', '')
            })
    
    # 手动配置数据源
    col1, col2 = st.columns(2)
    with col1:
        db_type = st.selectbox(
            '数据库类型',
            options=list(DB_TYPES.keys()),
            format_func=lambda x: DB_TYPES[x]['name'],
            key='backup_db_type',
            index=list(DB_TYPES.keys()).index(db_config.get('type', 'postgresql'))
        )
        db_config['type'] = db_type
        
        db_config['host'] = st.text_input('主机地址', db_config.get('host', ''), key='backup_host')
        db_config['port'] = st.number_input('端口', value=db_config.get('port', DB_TYPES[db_type]['default_port']), key='backup_port')
    with col2:
        db_config['user'] = st.text_input('用户名', db_config.get('user', ''), key='backup_user')
        db_config['password'] = st.text_input('密码', db_config.get('password', ''), key='backup_password', type='password')
        db_config['database'] = st.text_input('数据库名', db_config.get('database', ''), key='backup_database')
    
    # 测试连接按钮
    if st.button('测试连接', key='backup_test_connection'):
        with st.spinner('正在测试连接...'):
            if test_connection(db_config):
                st.success('连接成功！')
            else:
                st.error('连接失败，请检查配置是否正确')
    
    # 备份配置
    st.subheader('备份配置')
    col1, col2 = st.columns(2)
    with col1:
        # 默认获取当前目录
        output_backup_dir = os.path.join(os.getcwd(),'backup')
        if not os.path.exists(output_backup_dir):
            os.makedirs(output_backup_dir)
        output_dir = st.text_input('备份文件保存路径', output_backup_dir)

        compress = st.checkbox('压缩备份文件', value=True)
        tables = st.text_area('要备份的表名（每行一个，留空表示备份所有表）')
    with col2:
        data_only = st.checkbox('仅备份数据', value=True)
        column_inserts = st.checkbox('使用INSERT语句格式', value=True)
    
    # 执行备份
    if st.button('开始备份', type='primary'):
        try:
            with st.spinner('正在备份数据...'):
                table_list = [t.strip() for t in tables.split('\n') if t.strip()] if tables.strip() else None
                if db_config['type'] == 'postgresql':
                    for table in table_list:
                        print(f'备份表: {table}')
                        # 获取print输出
                        sys.stdout = st.empty()
                        
                        backup_file = pg_dump(
                            host=db_config['host'],
                            port=db_config['port'],
                            user=db_config['user'],
                            password=db_config['password'],
                            dbname=db_config['database'],
                            output_dir=os.path.join(output_dir, f'{table}.sql'),
                            data_only=data_only,
                            column_inserts=column_inserts,
                            include_table=[table]
                    )
                        if backup_file:
                            st.success(f'备份成功！\n文件保存在：{backup_file}',icon="🔥")
                        else:
                            st.error('备份失败',icon="🚨")
                else:  # MySQL
                    backup_file = dm.mysqldump(
                        host=db_config['host'],
                        port=db_config['port'],
                        user=db_config['user'],
                        password=db_config['password'],
                        dbname=db_config['database'],
                        output_dir=output_dir,
                        single_transaction=True,
                        no_data=not data_only,
                        extended_insert=not column_inserts
                    )
                
                # 压缩备份文件
                # if compress:
                #     backup_file = zip_files([backup_file])
                
        except Exception as e:
            st.error(f'备份失败: {str(e)}',icon="🚨")

def server():
    st.set_page_config(page_title='数据同步工具', layout='wide')
    
    # 初始化配置
    init_connection_config()
    
    # 添加侧边栏导航
    st.sidebar.title('Datamation')
    page = st.sidebar.radio('选择功能', ['数据同步', '数据比对', '数据结构比对', '数据备份'])
    
    if page == '数据同步':
        sync_data()
    elif page == '数据比对':
        compare_data()
    elif page == '数据结构比对':
        compare_structure()
    else:
        backup_data()

if __name__ == '__main__':
    server()