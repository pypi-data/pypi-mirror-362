#! /usr/bin/env python
# -*- coding: utf-8 -*-
        

import os
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody,FileAttachment
class exchange(object):
    def __init__(self,user=None,passwd =None):
        self.user = user if user else os.environ.get('mail_user','')
        self.passwd = passwd if passwd else os.environ.get('mail_passwd','')
        
    def login(self,user=None,passwd =None,):
        # 生成账户对象
        creds = Credentials(username=self.user,password=self.passwd)
        self.account = Account(primary_smtp_address = self.user,credentials=creds,autodiscover=True, access_type=DELEGATE )
        return True

    def execute(self,subject,to=[],cc=[],bcc=[],file=None,file_sub =None,text='',html=''):
        # 创建邮件主体
        m = Message(account=self.account,subject=subject,
                    to_recipients= [Mailbox(email_address= n) for n in  to],
                    cc_recipients= [Mailbox(email_address= n) for n in  cc],  # Simple strings work, too
                    bcc_recipients=[Mailbox(email_address= n) for n in  bcc],
                    body = text
                   )
        # 添加附件
        if file:
            if isinstance(file,(list)):
                files = file
            elif isinstance(file,str):
                files = [file]
            for f in files:
                m.attach(FileAttachment(name=os.path.basename(f),content=open(f, 'rb').read(),is_inline=False,content_id=os.path.basename(f)))

        # 添加引用资源
        if file_sub:
            if isinstance(file_sub,(list)):
                file_sub_ist = file_sub
            elif isinstance(file_sub,(str)):
                file_sub_ist = [file_sub]
                for f in file_sub_ist:
                    m.attach(FileAttachment(name=os.path.basename(f),content=open(f, 'rb').read(),is_inline=True,content_id=os.path.basename(f)))

        if html:
            m.body = HTMLBody(html)

        # 发送邮件
        m.send_and_save()
        return True
