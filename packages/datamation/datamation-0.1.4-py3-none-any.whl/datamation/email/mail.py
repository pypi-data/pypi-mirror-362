
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os   
import re
import io
import pathlib
from pathlib import Path

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.headerregistry import AddressHeader
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders

import imaplib
from email.parser import BytesParser, Parser
from email.policy import default,SMTP,SMTPUTF8,strict,HTTP
from collections.abc import Iterable    # 可迭代属性 验证参数

import time
import concurrent.futures
import logging

loggin = logging.getLogger(__name__)

class to_mail(object):
    '''邮件发送

    完成功能：

    - 构建邮件并且发送
    - 支持纯文本 html 图片 附件

    Examples
    --------
    >>> # 示例1
    >>> import datamation as dm
    >>> tm = dm.to_mail(user,passwd,host)
    >>> tm.name('hello word',to = ['xxx@xx.com','xxx@xxx.com'],
                             cc=  ['xxx@xx.com','xxx@xxx.com'],
                             bcc=  ['xxx@xx.com','xxx@xxx.com'],
               showname = 'datamation')
    >>> tm.add_text('hello word')
    >>> tm.add_html('<p> hello word</p> <img src=cid:image001.jpg style="height:71px; width:116px" />')
    >>> tm.add_related({'image001.jpg':'data/image001.jpg'}) # 添加在html中引用显示的图片内容
    >>> tm.add_attachment({'data.xlsx':'/data/data.xlsx'}) # 添加附件
    >>> tm.send()
    >>> # 示例2
    >>> import datamation as dm
    >>> tm = dm.to_mail(user,passwd,host)
    >>> tm.send('hello word',
                 to = ['xxx@xx.com'],
                 cc=  [''],
                 bcc= [''],
                 showname = 'datamation',
                 related = {'image001.jpg':'data/image001.jpg'},
                 attachment = {'data.xlsx':'/data/data.xlsx'})

    '''
    def __init__(self,user=None,passwd =None,host=None,port=None):
        '''初始化邮件发送对象

        Parameters
        ----------
        user : str
            邮箱账号 如果没有设置则尝试从环境变量中获取 mail_user
        passwd : str
            邮箱密码 如果没有设置则尝试从环境变量中获取 mail_passwd
        host : str
            邮箱服务器地址 例如：smtp.qq.com 如果没有设置则尝试从环境变量中获取 mail_host
        port : int
            邮箱服务器端口 例如：465 如果没有设置则尝试从环境变量中获取 mail_port
        '''
        self.host = host if host else os.environ.get('mail_host','')
        self.port = host if port else os.environ.get('mail_port','')
        self.user = user if user else os.environ.get('mail_user','')
        self.passwd = passwd if passwd else os.environ.get('mail_passwd','')

        self.error = []
        self.msg = MIMEMultipart('mixed') #alternative

    def login(self,user=None,passwd =None,host=None,port=None):
        '''进行邮件服务器登录 使用协议类型为 IMAP SMTP 
        '''
        user = user if user else self.user

        passwd = passwd if passwd else self.passwd
        host = host if host else self.host
        if port:
            self.port = port
        if self.port:
            self.conn = smtplib.SMTP_SSL(self.host,self.port)
            self.conn.login(user,passwd)
        else:
            self.conn = smtplib.SMTP_SSL(self.host)
            self.conn.login(user,passwd)
        return True

    def logout(self):
        '''关闭和邮箱服务器的连接
        '''
        self.conn.close()

    def name(self,subject,to=[],cc=[],bcc = [],showname='',*args,**kwags):
        '''收发件人

        Parameters
        -----------
        subject : str
            邮件主题
        to ：list 
            收件人
        cc : list
            抄送人
        bcc : list
            密送人
        showname : str
            在对方处显示的发件人昵称
        '''
        self.msg['Subject'] = Header(subject, 'utf-8')

        self.to = ';'.join(to)
        self.cc = ';'.join(cc)
        self.bcc = ';'.join(bcc)
        self.msg['to'] = self.to
        self.msg['cc'] = self.cc
        self.msg['bcc'] = self.bcc
        self.msg['from'] = formataddr([showname,self.user])
        
    def add_text(self,content='',*args,**kwags):
        '''邮件正文

        Parameters
        ----------
        txt : str
            邮件正文
        '''
        content = MIMEText(content, 'plain', 'utf-8')  # utf-8
        self.msg.attach(content)

    def add_html(self,content='',*args,**kwags):
        '''邮件中的html内容

        Parameters
        -----------
        htm: str
            HTML文本字符串 如果需要引用图片 需要将图片定义放于HTML之后
        '''
        if content:
            content = MIMEText(content,"html","utf-8")
            content["Content-Type"] = 'text/html'
            self.msg.attach(content) 
        
    def add_related(self,files = {},content_type ='image/jpeg'):
        '''引用的资源 使用引用图片时需要先定义HTML

        Parameters
        ----------
        files：list
            文件路径列表
        '''
        open_file = {io.BytesIO:lambda x:x.getvalue(),
                     bytes:lambda x:x,
                     str:lambda x:open(x, 'rb').read(),
                     pathlib.PosixPath:lambda x:open(x, 'rb').read(),
                     }

        for n,v in files.items():
            msgImage = MIMEImage(open_file[type(v)](v))
            msgImage["Content-Type"] = f'{content_type};name={n}'
            msgImage["Content-Description"] = f'{n}'
            msgImage["Content-Disposition"] = f'inline; filename="{n}"'
            msgImage.add_header('Content-ID',n)
            self.msg.attach(msgImage)
        return True
 
    def add_attachment(self,files = {}): 
        '''添加文件作为附件

        Parameters
        -------------
        flies: dict
               - key = 文件名称 
               - value = BytesIO  or  bytes or pathlib.PosixPath or str
               接受多种类型的的输入格式 列表 字典 元组 
               
               文件类型也可以是多样的 字符串 二进制对象  BytesIO 其中字符串 二进制对象等没有文件名的对象类型 需要指定文件名参数
        '''
        open_file = {io.BytesIO:lambda x:x.getvalue(),
                     bytes:lambda x:x,
                     str:lambda x:open(x, 'rb').read(),
                     pathlib.PosixPath:lambda x:open(x, 'rb').read(),
                     }
        for n,v in files.items():
            content = MIMEApplication(open_file[type(v)](v))
            content["Content-Type"] = 'application/octet-stream'
            content.add_header('Content-Disposition', 'attachment',filename=Header(n, 'utf-8').encode())
            self.msg.attach(content)
        return True

    def send(self,subject ='',to=[],cc=[],bcc=[],showname='',text = '',html='',related={},files = {}):
        '''邮件发送
        '''
        if any([subject,to,cc,bcc]):
            self.name(subject,to,cc,bcc,showname)
        if text:
            self.add_text(content = text)
        if html:
            self.add_html(content = html)
        if related:
            self.add_related(files = related)
        if files:
            self.add_attachment(files)

        try:
            self.login()
            self.conn.sendmail(self.user, self.to+self.cc+self.bcc, self.msg.as_string())
            return True
        finally:
            try:
                self.msg = MIMEMultipart('mixed')
                self.logout()
            except Exception as e :
                print(e)
                return False

class get_mail(object):
    '''邮件获取和解析

    功能

    - 查看邮件基本信息 收发件人 主题 时间

    - 判断是否存在附件，附件下载解析保存。

    - 正文内容的查看

    Returns
    -------
    class 
        一个直观的email操作对象
    '''
    def __init__(self,user=None,passwd =None,host=None,port=None):
        self.host = host if host else os.environ.get('mail_host','')
        self.port = port if port else os.environ.get('mail_port','')
        self.user = user if user else os.environ.get('mail_user','')
        self.passwd = passwd if passwd else os.environ.get('mail_passwd','')

    def login(self,user=None,passwd =None,host=None,port=None):
        '''进行邮件服务器登录

        支持协议类型为 IMAP SMTP
        
        '''
        user = user if user else self.user
        passwd = passwd if passwd else self.passwd
        host = host if host else self.host
        port = host if host else self.host
        if port:
            self.conn = imaplib.IMAP4_SSL(host,port)
        else:
            self.conn = imaplib.IMAP4_SSL(self.host)
        self.conn.login(user,passwd)
        return True
    
    def logout(self):
        '''关闭和邮箱服务器的连接
        '''
        self.conn.close()
        self.conn.logout()

    def select(self,mailbox = 'INBOX'):
        '''返回指定文件夹的全部邮件编号列表 默认为收件夹

        Parameters
        -----------
        mailbox : str
            文件夹名称 仅支持英文

        Returns
        --------
        list 
            所有邮件的编号
        '''
        self.conn.select(mailbox = mailbox)
        typ , data = self.conn.search(None, 'ALL')
        return list(map(int,data[0].split()))


    def msg(self,id,head = False):
        ''''根据参数id 取回邮件内容 默认全部解析

        Parameters
        -----------
        id : int
            int类型 标量或者可迭代对象，当id值为可迭代对象时返回值为字典
        head : bool
            为True时 只解析头部

        Returns
        -------
        返回邮件对象 msg
        '''
        typ, data = self.conn.fetch(str(int(id)), '(RFC822)')
        msg = BytesParser(policy=SMTP).parsebytes(data[0][1],headersonly = head)
        return msg

    def text(self,msg,pre = 'plain'):
        '''返回主要内容 解析顺序为 html > plain > related

        Parameters
        ----------
        msg ：msg
            邮件对象

        Returns
        -------
        str
            返回邮件正文的内容
        '''
        sort = {'html':['html','plain','related'],'plain':['plain','html','related']}
        content = msg.get_body(preferencelist= sort.get(pre,['plain','html','related'])).get_content()
        return content

    def text_subtype(msg):
        ''' 子内容

        Parameters
        -----------
        msg : msg
            根据子类型返回一个数字编号内容类型为后缀名的字典,一般多为图片

        Returns
        -------
        dict
            返回值为以数字为编号的字典 值为邮件中的附带内容
        '''
        data = {}
        num = 0
        for x in msg.iter_attachments():
            data[str(num)+'.'+ x.get_content_subtype()] = x.get_content()
            num+1
        return data
            
    def attachment(self,msg):
        '''获取邮件附件

        Parameters
        ----------

        msg : msg
            邮件对象
         
        Returns
        -------
        list
            邮件附件的列表
        '''
        file = []
        for n in msg.iter_attachments():
            if n.is_attachment():
                file.append(n.get_filename())
        return file

    def attachment_save(self,msg,path):
        '''附件保存 

        Parameters
        -----------
        msg : msg
            邮件对象
        path : str
            保存路径 path

        Returns
        --------
        dict  
                返回文件路径和存在状态的指示 
                key: 附件保存的文件路径
                value: 所保存文件是否存在

        '''
        file = {}
        
        for n in msg.iter_attachments():
            if n.get_content_disposition() == 'attachment':
                with open(Path(path)/n.get_filename(), 'wb') as f:
                    f.write(n.get_payload(decode=True))
                    file[Path(path)/n.get_filename()] = (Path(path)/n.get_filename()).exists()
        return file

    def info(self,ampunt:int= 10,head:list = None):
        '''返回邮件基本信息 收发件人 主题 日期 邮件编号

        Parameters
        ----------
        ampunt : int
            需要返回最近邮件的数量
        '''
        # 如果是可迭代对象则认为此对象为邮件编号集合
        if isinstance(ampunt,Iterable): 
            info_list = ampunt

        elif isinstance(ampunt,int):
            info_list = self.select()[:-ampunt-1:-1]

        msgs = [self.msg(int(n),head= True) for n in info_list]
        res_mail = {'id':info_list,'msg':msgs}

        head = head if head else ['from','To','cc','Subject','date']
        for n in head:
            res_mail[n] = [x.get(n,None)for x in msgs]

        return res_mail
    
    def monitor(self,task:list):
        '''邮件监听

        此函数仅提供持续监听新邮件功能 在有新邮件时触发执行传入的函数列表 使用while持续运行 用户可自行将其放置在后台
        
        Parameters
        -----------
        task : list of 可迭代对象
            传入无参回调函数 

        '''
        t = time.time()

        therd = concurrent.futures.ThreadPoolExecutor(5)

        col = '\033[1;31m'
        col_end = '\033[0m'
        new_mail = max(self.select())
        loggin.info('当前最新一封邮件为：',new_mail,self.text(self.msg(new_mail)))
        def f_task(f):
            try:
                f()
            except Exception as e:
                loggin.error(f,e)

        err = []

        loggin.info(col,'【开启邮件监听...】',col_end)
        status = lambda: print(col,'监听中...',col_end) 
        while 1:    
            if time.time()-t > 600:
                t = time.time()
            try:
                new = self.select()[-1]
            except KeyboardInterrupt:
                loggin.info('\n',col,'【结束监听服务...】',col_end,'\n')
                sys.exit()

            except Exception as e:
                loggin.error(col,e,f'正在第【{len(err)}】次重试登录...',col_end)
                err.append(e)
                time.sleep(3)
                self.login()

            if  new_mail< new:
                new_mail = new
                therd.map(f_task,task) # 在子线程处理事件
                loggin.info('事件已添加子线程处理')
                status()

            # 防止文件夹之间移动 导致邮件数量变化的差异
            elif new_mail > new:
                loggin.info('文件夹邮件有异常变动... \n 最新邮件编号由：{new_mail} 调整为: {new}')
                new_mail = new
                loggin.info(f'当前最新邮件为：[{new_mail}]')
                status()
