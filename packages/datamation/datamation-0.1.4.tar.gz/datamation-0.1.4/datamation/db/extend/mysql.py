import subprocess
import os
import datetime

def mysqldump(
    host, user, password, dbname, output_dir,
    port=3306, charset='utf8', single_transaction=True,
    quick=True, lock_tables=False, no_data=False,
    add_drop_table=True, extended_insert=True, 
    disable_keys=True, routines=False, events=False,
    compress=False,all_databases = False,skip_triggers = False
):
    """
    备份MySQL数据库的函数
    
    参数:
    host (str): 数据库主机地址
    user (str): 数据库用户名
    password (str): 数据库密码
    dbname (str): 要备份的数据库名称
    output_dir (str): 备份文件存放的目录
    port (int): 数据库端口，默认为3306
    charset (str): 字符集，默认为utf8
    single_transaction (bool): 是否使用单一事务，默认为True
    quick (bool): 是否使用快速导出，默认为True
    lock_tables (bool): 是否锁定表，默认为False
    no_data (bool): 是否不导出数据，只导出结构，默认为False
    add_drop_table (bool): 是否添加DROP TABLE语句，默认为True
    extended_insert (bool): 是否使用扩展插入语句，默认为True
    disable_keys (bool): 是否禁用键，默认为True
    routines (bool): 是否导出存储过程和函数，默认为False
    events (bool): 是否导出事件，默认为False
    compress (bool): 如果为True，使用压缩
    all_databases (bool): 如果为True，备份所有数据库
    skip_triggers (bool): 如果为True，不导出触发器

    返回:
    str: 备份文件的完整路径
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成备份文件名
    backup_file = os.path.join(output_dir, f"{dbname}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql")
    
    # 构建mysqldump命令
    dump_cmd = [
        "mysqldump",
        f"--host={host}",
        f"--user={user}",
        f"--password={password}",
        f"--port={port}",
        f"--default-character-set={charset}",
    ]
    
    if single_transaction:
        dump_cmd.append("--single-transaction")
    if quick:
        dump_cmd.append("--quick")
    if lock_tables:
        dump_cmd.append("--lock-tables")
    if no_data:
        dump_cmd.append("--no-data")
    if add_drop_table:
        dump_cmd.append("--add-drop-table")
    if extended_insert:
        dump_cmd.append("--extended-insert")
    if disable_keys:
        dump_cmd.append("--disable-keys")
    if routines:
        dump_cmd.append("--routines")
    if events:
        dump_cmd.append("--events")
    
    dump_cmd.append(dbname)
    
    # 执行mysqldump命令并将输出重定向到文件
    with open(backup_file, 'w') as output_file:
        result = subprocess.run(dump_cmd, stdout=output_file, stderr=subprocess.PIPE, text=True)
        
        # 检查是否有错误输出
        if result.returncode != 0:
            print(f"备份失败: {result.stderr}")
            return None
    
    print(f"备份成功: {backup_file}")
    return backup_file

def mysql(host, user, password, dbname, backup_file, port=3306, charset='utf8'):
    """
    执行MySQL文件 可以用于恢复数据库和数据导入
    
    参数:
    host (str): 数据库主机地址
    user (str): 数据库用户名
    password (str): 数据库密码
    dbname (str): 要恢复的数据库名称
    backup_file (str): 备份文件的路径
    port (int): 数据库端口，默认为3306
    charset (str): 字符集，默认为utf8
    
    返回:
    bool: 恢复是否成功
    """
    # 构建mysql命令
    restore_cmd = [
        "mysql",
        f"--host={host}",
        f"--user={user}",
        f"--password={password}",
        f"--port={port}",
        f"--default-character-set={charset}",
        dbname
    ]
    
    # 执行mysql命令并将备份文件作为输入
    with open(backup_file, 'r') as input_file:
        result = subprocess.run(restore_cmd, stdin=input_file, stderr=subprocess.PIPE, text=True)
        
        # 检查是否有错误输出
        if result.returncode != 0:
            print(f"恢复失败: {result.stderr}")
            return False
    
    print(f"恢复成功: {dbname}")
    return True

def mysql_load(
    host, user, password, dbname, table_name, data_file,
    port=3306, columns=None, character_set=None, fields_terminated_by=",",
    fields_enclosed_by=None, fields_escaped_by="\\", lines_starting_by=None,
    lines_terminated_by="\n", ignore_lines=0, replace=False, local=False,
    low_priority=False, concurrent=False, set_options=None
):
    """
    使用mysql的load data方式加载数据到MySQL表的函数

    参数:
    host (str): 数据库主机地址
    user (str): 数据库用户名
    password (str): 数据库密码
    dbname (str): 数据库名称
    table_name (str): 表名称
    data_file (str): 数据文件的路径
    port (int): 数据库端口，默认为3306
    columns (list): 要加载的列的列表
    character_set (str): 使用的字符集
    fields_terminated_by (str): 列的分隔符，默认值为","
    fields_enclosed_by (str): 列的引用符，默认值为None
    fields_escaped_by (str): 列的转义符，默认值为"\\"
    lines_starting_by (str): 行的开始符，默认值为None
    lines_terminated_by (str): 行的结束符，默认值为"\n"
    ignore_lines (int): 忽略的行数，默认值为0
    replace (bool): 如果为True，使用REPLACE语句而不是INSERT语句，默认值为False
    local (bool): 如果为True，使用LOCAL关键字，默认值为False
    low_priority (bool): 如果为True，使用LOW_PRIORITY关键字，默认值为False
    concurrent (bool): 如果为True，使用CONCURRENT关键字，默认值为False
    set_options (dict): 要设置的列值映射字典，默认值为None
    """
    # 构建MySQL命令
    load_cmd = [
        "mysql",
        f"--host={host}",
        f"--port={port}",
        f"--user={user}",
        f"--password={password}",
        dbname
    ]

    # 创建LOAD DATA命令
    load_data_sql = f"LOAD DATA {'LOCAL ' if local else ''}INFILE '{data_file}' "
    load_data_sql += f"{'REPLACE' if replace else 'IGNORE' if ignore_lines > 0 else ''} INTO TABLE {table_name} "

    if low_priority:
        load_data_sql += "LOW_PRIORITY "
    if concurrent:
        load_data_sql += "CONCURRENT "

    if character_set:
        load_data_sql += f"CHARACTER SET {character_set} "

    if fields_terminated_by:
        load_data_sql += f"FIELDS TERMINATED BY '{fields_terminated_by}' "
    if fields_enclosed_by:
        load_data_sql += f"ENCLOSED BY '{fields_enclosed_by}' "
    if fields_escaped_by:
        load_data_sql += f"ESCAPED BY '{fields_escaped_by}' "

    if lines_starting_by:
        load_data_sql += f"LINES STARTING BY '{lines_starting_by}' "
    if lines_terminated_by:
        load_data_sql += f"TERMINATED BY '{lines_terminated_by}' "

    if ignore_lines > 0:
        load_data_sql += f"IGNORE {ignore_lines} LINES "

    if columns:
        columns_str = ", ".join(columns)
        load_data_sql += f"({columns_str}) "

    if set_options:
        set_options_str = ", ".join([f"{col} = {val}" for col, val in set_options.items()])
        load_data_sql += f"SET {set_options_str}"

    load_cmd.append(f"-e \"{load_data_sql}\"")

    # 执行MySQL命令
    result = subprocess.run(load_cmd, stderr=subprocess.PIPE, text=True)

    # 检查是否有错误输出
    if result.returncode != 0:
        print(f"数据加载失败: {result.stderr}")
        return False
    
    print(f'加载成功: {data_file}')
    print(f"数据已加载入库: {dbname}.{table_name}")
    return True
