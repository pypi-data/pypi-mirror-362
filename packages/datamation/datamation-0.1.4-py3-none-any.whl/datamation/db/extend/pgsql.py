from datamation import table_basic
import re

import subprocess
import os
import datetime

try:
    import psycopg2
    import psycopg2.extras
    psycopg2.paramstyle = 'format'
    psycopg2.extensions.register_adapter(list, psycopg2.extras.Json)
    psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)

except ImportError:
    pass
try:
    import psycopg
    from psycopg.types.json import Jsonb, set_json_dumps, set_json_loads
    psycopg.paramstyle = 'format'
except ImportError:
    pass


class pgtable(table_basic):
     '''基于psycopg2 使用特殊的execute_batch批量插入方法 比原生executemany方法性能更高'''
     def general_executemany(self,operation,seq):
        '''
        Parameters
        ----------
        operation : str
            sql语句
        seq : list
            数据

        Returns
        -------
        None
        
        '''
        conn = self.conn_pool.connect() if self.conn_pool else self.conn
        cur = conn.cursor()
        # 如果数据执行失败，则回滚所有数据
        try:
            for _ in range(3):
                try:
                    psycopg2.extras.execute_batch(cur,operation,seq,page_size=len(seq))
                    #psycopg2.extras.execute_values(cur,re.sub('\(%s.*\%s\)','%s',operation),seq,page_size=20000)
                    conn.commit()
                    break
                except Exception as e:
                    if _ == 2:
                        print('异常:',e)
                        print('异常数据:',operation,seq[:1])
                        raise e
                    try:
                        conn.rollback()
                        conn.close()
                    finally:
                        conn = self.conn_pool.connect() if self.conn_pool else self.conn
                        cur = conn.cursor()
                        
        except Exception as e:
            if self.strict:
                conn.rollback()
                raise e
            else:
                self.err_rows[e].append((operation,seq))
                pass
        finally:
            cur.close()
            if self.conn_pool:
                conn.close()

class pgtable3(table_basic):
     '''基于psycopg3 采用copy_from方法批量插入数据 来提高性能'''
     def general_executemany(self,operation,seq):
        '''
        Parameters
        ----------
        operation : str
            sql语句
        seq : list
            数据

        Returns
        -------
        None
        
        '''
        conn = self.conn_pool.connect() if self.conn_pool else self.conn
        cur = conn.cursor()
        # 如果数据执行失败，则回滚所有数据
        try:
            for _ in range(3):
                try:
                    col_str = ','.join( [self.rename.get(n,n) for n in self.columns_all] )
                    sql_str = f"COPY {self.table_name} ({col_str}) FROM STDIN"
                    with cur.copy(sql_str) as copy:
                        for record in seq:
                            copy.write_row(record)
                    conn.commit()
                    break
                except Exception as e:
                    print(e)
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                    if 'timeout' in str(e).lower() or 'close' in str(e).lower():
                        conn = self.conn_pool.connect() if self.conn_pool else self.conn
                        cur = conn.cursor()
        except Exception as e:
            print(e)
            if self.strict:
                conn.rollback()
                raise e
            else:
                self.err_rows[e].append((operation,seq))
                pass
        finally:
            cur.close()
            if self.conn_pool:
                conn.close()

def pg_dump(
    host, user,password, dbname, output_dir,
    port=5432,format='plain', compress=False, blobs=False,
    clean=False, create=False, data_only=True,inserts = False,column_inserts = True, schema_only=False,
    encoding=None, exclude_table=None, exclude_schema=None,
    include_table=None, include_schema=None, no_owner=True,
    no_privileges=False, quote_all_identifiers=False, use_set_session_authorization=False,show_log=False
):
    """
    对pg_dump命令工具封装 进行备份PostgreSQL数据库的函数 
    
    Args:
        host (str): 数据库主机地址
        user (str): 数据库用户名
        password (str): 数据库密码
        dbname (str): 要备份的数据库名称
        output_dir (str): 备份文件存放的目录
        port (int): 数据库端口，默认为5432
        format (str): 备份文件格式，默认为plain（其他选项：custom, directory, tar）
        compress (bool): 是否压缩备份文件，默认为False
        blobs (bool): 是否包括大对象，默认为False
        clean (bool): 是否在恢复前清除数据库对象，默认为False
        create (bool): 是否在备份中创建数据库，默认为False
        data_only (bool): 是否仅备份数据，默认为False
        inserts (bool): 将数据转储为INSERT命令（而不是COPY）
        column_inserts (bool): 将数据转储为带有显式列名的INSERT命令（INSERT INTO table (column, ...) VALUES ...）
        schema_only (bool): 是否仅备份模式，默认为False
        encoding (str): 备份文件的编码
        exclude_table (list): 排除的表
        exclude_schema (list): 排除的模式
        include_table (list): 包含的表
        include_schema (list): 包含的模式
        no_owner (bool): 不设置对象的所有者
        no_privileges (bool): 不包括权限
        quote_all_identifiers (bool): 对所有标识符加引号
        use_set_session_authorization (bool): 使用SET SESSION AUTHORIZATION而不是ALTER OWNER
        
    Returns:
        str: 备份文件的完整路径
    """

    # 构建输出目录
    if os.path.isdir(output_dir):
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        backup_file = os.path.join(output_dir,f"{dbname}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.dump")
    else:
        backup_file = output_dir

    # 生成备份文件名
    #backup_file = os.path.join(output_dir,f"{dbname}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql")
    
    # 构建pg_dump命令
    dump_cmd = [
        "pg_dump",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        f"--format={format}",
        f"--file={backup_file}",
        "--no-password"
    ]
    
    if compress:
        dump_cmd.append("--compress=9")
    if blobs:
        dump_cmd.append("--blobs")
    if clean:
        dump_cmd.append("--clean")
    if create:
        dump_cmd.append("--create")
    if data_only:
        dump_cmd.append("--data-only")
    if inserts:
        dump_cmd.append("--inserts")
    if column_inserts:
        dump_cmd.append("--column-inserts")
    if schema_only:
        dump_cmd.append("--schema-only")
    if encoding:
        dump_cmd.append(f"--encoding={encoding}")
    if exclude_table:
        for table in exclude_table:
            dump_cmd.append(f"--exclude-table-data={table}")
    if exclude_schema:
        for schema in exclude_schema:
            dump_cmd.append(f"--exclude-schema={schema}")
    if include_table:
        for table in include_table:
            dump_cmd.append(f"--table={table}")
    if include_schema:
        for schema in include_schema:
            dump_cmd.append(f"--schema={schema}")
    if no_owner:
        dump_cmd.append("--no-owner")
    if no_privileges:
        dump_cmd.append("--no-privileges")
    if quote_all_identifiers:
        dump_cmd.append("--quote-all-identifiers")
    if use_set_session_authorization:
        dump_cmd.append("--use-set-session-authorization")
    
    dump_cmd.append(dbname)
    
    # 设置环境变量来传递密码
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    
    # 执行pg_dump命令
    result = subprocess.run(dump_cmd, stderr=subprocess.PIPE, text=True, env=env)
    if show_log:
        print(' '.join(result.args))
    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"备份失败: {result.stderr}")
        return None
    
    filesize = '体积:{} MB'.format(round(os.path.getsize(backup_file)/1024/1024,3))
    print(f"备份成功: {backup_file} ")
    print(filesize)
    
    # 清理环境变量
    del env["PGPASSWORD"]
    return backup_file

def pg_restore(
    host, user, password, dbname, backup_file, port=5432,
    clean=False, create=False, exit_on_error=False,
    format='custom', jobs=None, no_acl=False, no_comments=False,
    no_data_for_failed_tables=False, no_owner=False, no_privileges=False,
    if_exists=False, disable_dollar_quoting=False, disable_triggers=False,
    schema=None, section=None, single_transaction=False,
    superuser=None, table=None, use_list=None, verbose=False,
    data_only=False, index=None, list_only=False, oid_order=False,
    role=None, strict_names=False, use_set_session_authorization=False,
    extra_float_digits=None, funcname=None, use_remote_estimate=False
):
    """
    使用 pg_restore 恢复PostgreSQL数据库的函数
    
    Args:
        host (str): 数据库主机地址
        user (str): 数据库用户名
        password (str): 数据库密码
        dbname (str): 要恢复的数据库名称
        backup_file (str): 备份文件的路径
        port (int): 数据库端口，默认为5432
        clean (bool): 在恢复前清除数据库对象，默认为False
        create (bool): 在恢复中创建数据库，默认为False
        exit_on_error (bool): 在出错时退出，默认为False
        format (str): 备份文件的格式 (custom, directory, tar)
        jobs (int): 恢复时使用的并行作业数
        no_acl (bool): 不恢复权限，默认为False
        no_comments (bool): 不恢复注释，默认为False
        no_data_for_failed_tables (bool): 不恢复失败表的数据，默认为False
        no_owner (bool): 不恢复对象的所有者，默认为False
        no_privileges (bool): 不恢复权限，默认为False
        if_exists (bool): 如果对象存在则删除，默认为False
        disable_dollar_quoting (bool): 禁用美元符号引用，默认为False
        disable_triggers (bool): 禁用触发器，默认为False
        schema (str): 恢复的模式名称
        section (str): 恢复的部分 (pre-data, data, post-data)
        single_transaction (bool): 使用单一事务恢复，默认为False
        superuser (str): 超级用户角色名称
        table (str): 恢复的表名称
        use_list (str): 使用列表文件
        verbose (bool): 输出详细信息，默认为False
        data_only (bool): 仅恢复数据，默认为False
        index (str): 恢复的索引
        list_only (bool): 仅列出存档内容，默认为False
        oid_order (bool): 按OID顺序恢复，默认为False
        role (str): 以指定角色执行，默认为None
        strict_names (bool): 严格名称匹配，默认为False
        use_set_session_authorization (bool): 使用SET SESSION AUTHORIZATION而不是ALTER OWNER，默认为False
        extra_float_digits (int): 额外的浮点数位数，默认为None
        funcname (str): 恢复的函数名称
        use_remote_estimate (bool): 使用远程估计，默认为False
        
    Returns:
        bool: 恢复是否成功
    """
    # 构建pg_restore命令
    restore_cmd = [
        "pg_restore",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        f"--dbname={dbname}",  
        f"--format={format}",
        backup_file,
        "--no-password"
    ]

    if clean:
        restore_cmd.append("--clean")
    if create:
        restore_cmd.append("--create")
    if exit_on_error:
        restore_cmd.append("--exit-on-error")
    if jobs is not None:
        restore_cmd.append(f"--jobs={jobs}")
    if no_acl:
        restore_cmd.append("--no-acl")
    if no_comments:
        restore_cmd.append("--no-comments")
    if no_data_for_failed_tables:
        restore_cmd.append("--no-data-for-failed-tables")
    if no_owner:
        restore_cmd.append("--no-owner")
    if no_privileges:
        restore_cmd.append("--no-privileges")
    if if_exists:
        restore_cmd.append("--if-exists")
    if disable_dollar_quoting:
        restore_cmd.append("--disable-dollar-quoting")
    if disable_triggers:
        restore_cmd.append("--disable-triggers")
    if schema:
        restore_cmd.append(f"--schema={schema}")
    if section:
        restore_cmd.append(f"--section={section}")
    if single_transaction:
        restore_cmd.append("--single-transaction")
    if superuser:
        restore_cmd.append(f"--superuser={superuser}")
    if table:
        restore_cmd.append(f"--table={table}")
    if use_list:
        restore_cmd.append(f"--use-list={use_list}")
    if verbose:
        restore_cmd.append("--verbose")
    if data_only:
        restore_cmd.append("--data-only")
    if index:
        restore_cmd.append(f"--index={index}")
    if list_only:
        restore_cmd.append("--list")
    if oid_order:
        restore_cmd.append("--oid-order")
    if role:
        restore_cmd.append(f"--role={role}")
    if strict_names:
        restore_cmd.append("--strict-names")
    if use_set_session_authorization:
        restore_cmd.append("--use-set-session-authorization")
    if extra_float_digits is not None:
        restore_cmd.append(f"--extra-float-digits={extra_float_digits}")
    if funcname:
        restore_cmd.append(f"--function={funcname}")
    if use_remote_estimate:
        restore_cmd.append("--use-remote-estimate")
    
    # 设置环境变量来传递密码
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    
    # 执行pg_restore命令
    result = subprocess.run(restore_cmd, stderr=subprocess.PIPE, text=True, env=env)
    
    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"恢复失败: {result.stderr}")
        return False
    
    print(f"恢复成功: {dbname}")
    # 清理环境变量
    del env["PGPASSWORD"]
    return True

def pg_psql(
    host, user, password, dbname, input_file, port=5432,
):
    """
    恢复PostgreSQL数据库的函数
    
    参数:
    host (str): 数据库主机地址
    user (str): 数据库用户名
    password (str): 数据库密码
    dbname (str): 要恢复的数据库名称
    input_file (str): 执行sql文件的路径
    port (int): 数据库端口，默认为5432
    
    返回:
    bool: 恢复是否成功
    """
    # 构建psql命令
    execute_cmd = [
        "psql",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        f"--dbname={dbname}",
        f"--file={input_file}",
    ]
    
    # 设置环境变量来传递密码
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    
    # 执行psql命令
    result = subprocess.run(execute_cmd,text=True, env=env)
    
    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"执行失败: {result.stderr}")
        return False
    
    print(f"执行成功: {dbname}")
    # 清理环境变量
    del env["PGPASSWORD"]
    return True

def pg_copy_to(
    host, user, password, dbname,output_dir,table_name='', query='',
    port=5432, columns=None, delimiter=",", null_str="\\N", header=False, quote='"', 
    escape="\\", force_quote=None, encoding='utf-8', format="csv", oids=False, 
    where=None, 
):
    """
    使用\copy命令从PostgreSQL表导出数据到文件的函数

    Args:
        host (str): 数据库主机地址
        user (str): 数据库用户名
        password (str): 数据库密码
        dbname (str): 数据库名称
        table_name (str): 表名称
        output_dir (str): 输出数据文件的路径
        port (int): 数据库端口，默认为5432
        columns (list): 要导出的列的列表，默认值为None
        delimiter (str): 列的分隔符，默认值为","
        null_str (str): 用于表示NULL值的字符串，默认值为"\\N"
        header (bool): 如果为True，输出数据文件的第一行包含列名，默认值为False
        quote (str): 用于引用字段的字符，默认值为'"'
        escape (str): 用于转义的字符，默认值为"\\"
        force_quote (list): 要强制加引号的列名列表，默认值为None
        encoding (str): 输出数据文件的编码，默认值为utf-8
        format (str): 文件格式，默认为"csv"
        oids (bool): 如果为True，导出对象ID，默认值为False
        where (str): 数据过滤条件，默认值为None
        query (str): 自定义查询语句，默认值为None
    """
    # 设置环境变量来传递密码
    env = os.environ.copy()
    env["PGPASSWORD"] = password

    # 构建psql命令
    copy_cmd = [
        "psql",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        f"--dbname={dbname}",
        "-c",
    ]

    # 创建\copy命令
    if query:
        copy_sql = f"\\copy ({query}) "
    else:
        if table_name:
            copy_sql = f"\\copy {table_name} "
        else:
            raise ValueError("请提供表名或自定义查询语句")

    if columns and not query:
        columns_str = ", ".join(columns)
        copy_sql += f"({columns_str}) "
    
    if output_dir:
        if table_name:
            output_file = os.path.join(output_dir, f"{table_name.replace('.', '_')[:50]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{format}")
        else:
            output_file = os.path.join(output_dir, f"{query.replace('.', '_')[:50]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{format}")

    copy_sql += f"TO '{output_file}' WITH (FORMAT {format}, DELIMITER '{delimiter}', NULL '{null_str}'"

    if format == 'csv':
        if header:
            copy_sql += ", HEADER"

        if quote:
            copy_sql += f", QUOTE '{quote}'"

        if escape:
            copy_sql += f", ESCAPE '{escape}'"

        if force_quote:
            force_quote_str = ", ".join(force_quote)
            copy_sql += f", FORCE_QUOTE ({force_quote_str})"

    if format == 'text':
        if oids:
            copy_sql += ", OIDS"

    if encoding:
        copy_sql += f", ENCODING '{encoding}'"
        
    copy_sql += ")"

    if where and not query:
        copy_sql += f" WHERE {where}"

    copy_cmd.append(copy_sql)

    # 执行psql命令
    result = subprocess.run(copy_cmd, stderr=subprocess.PIPE, text=True,env=env)

    del env["PGPASSWORD"]

    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"数据导出失败: {result.stderr}")
        return False

    print(f"数据导出成功: {dbname}.{table_name}")
    print('输出文件:',output_file)
    return True

def pg_copy_from(
    host, user, password, dbname,input_file, table_name,
    port=5432, columns=None, delimiter=",", null_str="\\N", header=False, quote='"',
    escape="\\", force_quote=None, encoding='utf-8', format="csv", oids=False,
    where=None,
):
    """
    使用\copy命令从文件导入数据到PostgreSQL表的函数
    Args:
        host (str): 数据库主机地址
        user (str): 数据库用户名
        password (str): 数据库密码
        dbname (str): 数据库名称
        table_name (str): 表名称
        input_file (str): 输入数据文件的路径
        port (int): 数据库端口，默认为5432
        columns (list): 要导入的列的列表，默认值为None
        delimiter (str): 列的分隔符，默认值为","
        null_str (str): 用于表示NULL值的字符串，默认值为"\\N"
        header (bool): 如果为True，输入数据文件的第一行包含列名，默认值为False
        quote (str): 用于引用字段的字符，默认值为'"'
        escape (str): 用于转义的字符，默认值为"\\"
        force_quote (list): 要强制加引号的列名列表，默认值为None
        encoding (str): 输入数据文件的编码，默认值为utf-8

    """
    # 设置环境变量来传递密码
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    # 构建psql命令
    copy_cmd = [
        "psql",
        f"--host={host}",
        f"--port={port}",
        f"--username={user}",
        f"--dbname={dbname}",
        "-c",
    ]
    # 创建\copy命令
    copy_sql = f"\\copy {table_name} "
    if columns:
        columns_str = ", ".join(columns)
        copy_sql += f"({columns_str}) "
    copy_sql += f"FROM '{input_file}' WITH (FORMAT {format}, DELIMITER '{delimiter}', NULL '{null_str}'"
    if format == 'csv':
        if header:
            copy_sql += ", HEADER"
        if quote:
            copy_sql += f", QUOTE '{quote}'"
        if escape:
            copy_sql += f", ESCAPE '{escape}'"
        if force_quote:
            force_quote_str = ", ".join(force_quote)
            copy_sql += f", FORCE_QUOTE ({force_quote_str})"
    if format == 'text':
        if oids:
            copy_sql += ", OIDS"
    if encoding:
        copy_sql += f", ENCODING '{encoding}'"
    copy_sql += ")"
    if where:
        copy_sql += f" WHERE {where}"
    copy_cmd.append(copy_sql)
    # 执行psql命令
    result = subprocess.run(copy_cmd, stderr=subprocess.PIPE, text=True, env=env)
    del env["PGPASSWORD"]
    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"数据导入失败: {result.stderr}")
        return False
    print(f"数据导入成功: {dbname}.{table_name}")
    return True

def pg_copy_to_from(source_conn, target_conn, source_table: str, target_table: str,truncate:bool=False) -> int:
    """
    采用COPY方式 从源数据库同步表到目标数据库 
    
    需要表结构完全一致
    
    Parameters
    ----------
    source_conn : psycopg.Connection or callable
        源数据库连接对象
    target_conn : psycopg.Connection or callable
        目标数据库连接对象
    source_table : str
        源表名
    target_table : str
        目标表名
    
    Returns
    -------
    int
        同步的行数
    """
    # 连接到源数据库和目标数据库
    with source_conn() as conn1, target_conn() as conn2:
        # 构建COPY命令
        copy_from_sql = f"COPY {source_table} TO STDOUT (FORMAT BINARY)"
        copy_to_sql = f"COPY {target_table} FROM STDIN (FORMAT BINARY)"
        
        # 执行数据复制
        rows_copied = 0
        with conn1.cursor() as src_cur, conn2.cursor() as tgt_cur:
            if truncate:
                tgt_cur.execute(f"TRUNCATE TABLE {target_table}")
            with src_cur.copy(copy_from_sql) as src_copy, \
                 tgt_cur.copy(copy_to_sql) as tgt_copy:
                # 逐块读取源数据并写入目标数据库
                for data in src_copy:
                    tgt_copy.write(data)
                    rows_copied += 1
    
    return rows_copied