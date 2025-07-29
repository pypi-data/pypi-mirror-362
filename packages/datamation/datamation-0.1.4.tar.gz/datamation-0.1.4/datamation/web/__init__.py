'''
Author: 李道然 qianxuanyon@hotmail.com
Date: 2025-03-18 14:23:25
LastEditors: 李道然 qianxuanyon@hotmail.com
LastEditTime: 2025-03-20 11:21:03
'''
import os
import sys
import subprocess
import click

@click.command()
@click.option("--port", default=8501, help="streamlit port")
def start(port):
    # 构造 streamlit run 命令
    # 获取本文件同目录下的sync_app.py文件
    
    # 获取本文件的绝对路径
    file_path = os.path.abspath(__file__)
    # 获取本文件的目录
    dir_path = os.path.dirname(file_path)
    # 获取sync_app.py的绝对路径
    sync_app_path = os.path.join(dir_path, "sync_app.py")

    cmd = [sys.executable, "-m", "streamlit", "run", sync_app_path, "--server.port", str(port)]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    start()