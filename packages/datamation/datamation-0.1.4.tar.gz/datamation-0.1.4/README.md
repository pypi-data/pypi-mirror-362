# Datamation

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic)

Datamation 是一个Python 数据处理工具库，专注于数据库操作、ETL数据同步和数据比对等功能。它提供了简单易用的方法，帮助开发者高效地处理数据迁移、同步等任务。

## 特性

- 支持不同数据库之间的大批量数据导入、导出和 ETL 数据同步
- 支持将关系型数据库数据导入到 ElasticSearch
- 提供数据库表结构差异比对，表数据差异比对，数据差异定位到行级
- 集成消息通知功能，支持邮件、钉钉、企业微信
- 提供灵活的数据转换和过滤功能

## 安装

### 基础安装

```bash
pip install datamation
```

## 基本使用

### 数据库连接

```python
import pymysql 
import datamation as dm

# 创建数据源连接
source_conn = lambda:pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='xxx',
    database='demo',
    port=13307,
    write_timeout = 50000,
    connect_timeout = 20000
)

# 创建目标数据库连接
target_conn = lambda:pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='xxx',
    database='demo',
    port=13306,
    read_timeout=50000,
    connect_timeout=10000
)
```

### 数据同步

#### 方式一：简单同步

```python
dm.sqlsync(
    source_conn=source_conn,
    src_table='table1',
    target_conn=target_conn,
    tag_table='table2',
    # filed_adapter ={dict:Json,list:Json}, # 字段类型转换
    batch_size=20000,  # 批量写入行数
    truncate=True      # 同步开始时使用truncate命令清空目标数据表
) 
```

#### 方式二：自定义同步

```python
source = dm.source_sql(source_conn, 'table1')
target = dm.table_basic(target_conn, 'table1', columns=['col1', 'col2', 'col3'], batch_size=20000)
for row in src:
    target.insert(row)
target.endload()
```

#### 数据导入到ElasticSearch

```python
from elasticsearch import Elasticsearch
es=Elasticsearch([{ "host":"xxx.xxx.xxx.xxx","port":xxxx}])

src = dm.source_sql(source_conn, 'table1')
target = dm.elastic_basic(es,index = 'table')
for row in src:
    target.insert(row)
target.endload()
```


#### postgreSQL高性能数据导入

```python
# pgtable类替代table_basic类，采用内部专有的批量方法来实现比pep249的executemany更高性能
# 只有psycopg2驱动需要 psycopg之后使用通用的table_basic类即可 
# 如果涉及到Jsonb字段，注意加参数filed_adapter ={dict:Json,list:Json}进行字段类型的转换

from datamation.db.extend import pgtable
from psycopg2.extras import Json

dm.sqlsync(
    source_conn=source_conn,
    src_table='table1',
    target_conn=target_conn,
    tag_table='table2',
    # filed_adapter ={dict:Json,list:Json}, # 字段类型转换
    batch_size=20000,  # 批量写入行数
    truncate=True,      # 同步开始时使用truncate命令清空目标数据表
    table_cls = pgtable

) 

source = dm.source_sql(source_conn, 'table1')
target = pgtable(target_conn, 'table1', columns=['col1', 'col2', 'col3'], batch_size=20000)
for row in src:
    target.insert(row)
target.endload()

```

### 数据比对

#### 表结构比对

基于 SQLAlchemy 的表结构差异比对：

```python

res = dm.get_sqldb_diff(source_conn,target_conn, "postgresql")
for sql in res:
    print(sql)
```

#### 数据内容比对

1. 数值类型主键比对：

```python
comp = dm.get_sqldata_diff2(source_conn, target_conn, 'tb_data', 'tb_data_copy1', compare_field='id')
print(comp)
```

2. UUID 类型主键比对：

```python
comp = dm.get_sqldata_diff1(source_conn, target_conn, 'tb_data', 'tb_data_copy1', compare_field='id')
print(comp)
```

3. 进行数据量比对：

```python
# 主键id为整数类型
import datamation as dm
comp = dm.get_sqldata_diff2(conn,conn,'yth_subject_copy1','yth_subject_copy2',
                            compare_field ='*',
                            source_dbms_hash=dm.dbms_hash_count,
                            target_dbms_hash=dm.dbms_hash_count,
                            partition_field='id')

print('输出差异结果',comp.result)
print(time.ctime())
```

### 消息通知

#### 钉钉通知

```python
import datamation as dm

# 创建钉钉机器人实例
ding = dm.to_dingtalk(webhook="钉钉机器人webhook地址", secret="安全设置的加签密钥")

# 发送文本消息
ding.send_text("Hello World", at_mobiles=["13800000000"], at_all=False)

# 发送Markdown消息
ding.send_markdown(
    title="标题",
    text="**加粗文本**\n普通文本\n![图片](https://img.png)",
    at_mobiles=["130xxxxxxxx"],
    at_all=False
)

# 发送图片消息
ding.send_image("/path/to/image.png")
```

#### 企业微信通知

```python
import datamation as dm

# 创建企业微信机器人实例
wechat = dm.to_wechat(webhook="企业微信机器人webhook地址")

# 发送文本消息
wechat.send_text("Hello World", mentioned_list=["@all"], mentioned_mobile_list=["13800138000"])

# 发送Markdown消息
wechat.send_markdown("**加粗文本**\n普通文本\n[链接](https://example.com)")

# 发送图片消息
wechat.send_image("/path/to/image.png")
```

#### 邮件通知

方式一：链式调用

```python
import datamation as dm

tm = dm.to_mail(user, passwd, host)
tm.name('hello world',
       to=['xxx@xx.com', 'xxx@xxx.com'],
       cc=['xxx@xx.com', 'xxx@xxx.com'],
       bcc=['xxx@xx.com', 'xxx@xxx.com'],
       showname='datamation')
tm.add_text('hello world')
tm.add_html('<p>hello world</p> <img src=cid:image001.jpg style="height:71px; width:116px" />')
tm.add_related({'image001.jpg': 'data/image001.jpg'})  # 添加在html中引用显示的图片内容
tm.add_attachment({'data.xlsx': '/data/data.xlsx'})    # 添加附件
tm.send()
```

方式二：一次性发送

```python
import datamation as dm

tm = dm.to_mail(user, passwd, host)
tm.send('hello world',
        to=['xxx@xx.com'],
        cc=[''],
        bcc=[''],
        showname='datamation',
        related={'image001.jpg': 'data/image001.jpg'},
        attachment={'data.xlsx': '/data/data.xlsx'})
```

### 数据备份

支持调用pg_dump命令进行PostgreSQL数据库备份,可以指定数据库环境、模式和表名，备份后自动压缩为zip文件。

```python
from datamation.db.extend import pg_dump

# 配置数据库连接信息
dbcfg = {
    'dev': {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'xxx',
        'host': '127.0.0.1',
        'port': '5432'
    }
}

# 备份指定表
pg_dump(
    dbname=dbcfg['dev']['dbname'],
    user=dbcfg['dev']['user'],
    password=dbcfg['dev']['password'],
    host=dbcfg['dev']['host'],
    port=dbcfg['dev']['port'],
    output_dir='/path/to/backup/file.sql',
    column_inserts=True,  # 使用INSERT语句格式
    compress=False,       # 是否压缩
    include_table=['schema.table_name']  # 指定要备份的表
)
```

## 许可证

BSD License
## 作者

lidaoran (qianxuanyon@hotmail.com)

