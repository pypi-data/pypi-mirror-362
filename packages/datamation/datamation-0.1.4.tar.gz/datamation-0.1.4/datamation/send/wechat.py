#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib

import requests

__all__ = ['work_wechat']

class work_wechat(object):
    '''企业微信机器人
    
    '''
    def __init__(self,url):
        self.url = url
        
    def imag(self,content):
        '''图片

        '''
        data = {"msgtype": "image",
                "image": {"base64": base64.b64encode(content),
                          "md5": hashlib.md5(content).hexdigest()
			}
                   }
        res = requests.post(self.url,json = data)
        return res.json()
    
    def text(self,content):
        '''文本

        '''
        data = {"msgtype": "text",
                "text": { "content": content}
               }
        res = requests.post(self.url,json = data)
        return res.json()
    
    def markdown(self,content):
        '''markdown

        '''
        data = {"msgtype": "markdown",
                "markdown": { "content": content}
               }
        res = requests.post(self.url,json = data)
        return res.json()

