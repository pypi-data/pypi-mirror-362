'''对数据库和表进行数据备份
'''
import sqlite3
from datamation import sqlsync,get_sqldb_diff
import datetime

import pickle

def adapt_py(obj):
    return pickle.dumps(obj)
def convert_py(obj):
    return pickle.loads(obj)

def backup_db_data(src_conn,filename = ''):
    '''备份数据库
    '''
    if not filename:
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.db'
    else:
        filename = filename+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.db'
    tag_conn = sqlite3.connect(filename)
    sync_script = get_sqldb_diff(src_conn,tag_conn)
    if sync_script:
        tag_conn.executescript(''.join(sync_script))
        tag_conn.commit()
    tables = tag_conn.execute("select name from sqlite_master where type='table' order by name").fetchall()
    for table in tables:
        sqlsync(src_conn,table[0],tag_conn,table[0],truncate = False)
    tag_conn.close()

# 恢复数据库数据
def restore_db_data(tag_conn,filename):
    '''恢复数据库
    '''
    src_conn = sqlite3.connect(filename)
    tables = src_conn.execute("select name from sqlite_master where type='table' order by name").fetchall()
    for table in tables:
        sqlsync(src_conn,table[0],tag_conn,table[0],truncate = False)
    src_conn.close()
    return True
