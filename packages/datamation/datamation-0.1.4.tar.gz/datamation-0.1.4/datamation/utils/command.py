#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import datamation as dm

tns = os.environ.get('tns')

def dbuldr(*args):
    dm.dbuldr(*args)

def csvldr(*args):
    dm.csvldr(*args)

parser = argparse.ArgumentParser(prog='dbldr',description="ETL tool \n 手工执行数据同步任务 补历史数据 历史数据回溯更新 ")
subparsers = parser.add_subparsers(title = 'operation',help = '功能选项')
parser_e = subparsers.add_parser('ldr', help='数据导出为文本')
parser_e.add_argument('-user','--user',help = '数据库连接字符串',required=True)
parser_e.add_argument('-sql','--sql',help = '表名或者sql语句 ',required=True)
parser_e.add_argument('-file','--file', default = '',help = '文件名称',required=True)
parser_e.add_argument('-batch_size','--batch_size', default = 50000 ,help = '每次批量插入行数  number',type = int)
parser_e.add_argument('-encod','--encod', default = 'utf-8' ,help = '编码',type = str)
parser_e.set_defaults(func = dbuldr)

parser_e = subparsers.add_parser('uldr', help='文本数据导入数据库')
parser_e.add_argument('-sql','--sql', default = '',help = '表名或者sql语句 ')
parser_e.add_argument('-file','--file', default = '',help = '文件名称')
parser_e.add_argument('-batch_size','--batch_size', default = 50000 ,help = '每次批量插入行数  number',type = int)
parser_e.add_argument('-encod','--encod', default = 'utf-8' ,help = '编码',type = str)
parser_e.set_defaults(func = csvldr)

args = parser.parse_args()
print(args)
