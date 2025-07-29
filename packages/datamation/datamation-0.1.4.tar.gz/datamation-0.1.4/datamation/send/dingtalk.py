
import time
import hmac
import hashlib
import base64
import urllib.parse
import urllib
import requests

class dingtalk():
    '''钉钉群机器人消息发送
    '''
    def __init__(self,url,secret=''):
        '''
        url:str
            钉钉群机器人的接口url
        secret:str
            签名值
        '''
        self.url = url
        self.__secret = secret
        
    def get_sign(self):
        timestamp = str(round(time.time() * 1000))
        secret = self.__secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp,sign
    
    def send_markdown(self,title,text,atMobiles = [],atUserIds = [],isAtAll = False):
        '''发送markdown类型消息

        Parameters
        -----------
        title:str
            首屏会话透出的展示内容
        text:str
            markdown格式的消息
        atMobiles:list
            被@人的手机号
        atUserIds:list  
            被@人的userid
        isAtAll:bool    
            @所有人时：true，否则为：false
        
        Examples
        -----------
        >>> from datamation.send import dingtalk
        >>> url = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx'
        >>> ding = dingtalk(url)
        >>> markdown = '# 今日任务\\n- [ ] 任务1\\n- [ ] 任务2\\n- [ ] 任务3'
        >>> ding.send_markdown('今日任务',markdown)
        '''
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":title,
                "text": text
            },
            "at": {
                "atMobiles":atMobiles,
                "atUserIds":atUserIds,
                "isAtAll": isAtAll
            }
        }
        return self.send(data)  
    
    def send_text(self,content,atMobiles = [],atUserIds = [],isAtAll = False):
        '''发送text类型消息
        '''
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles":atMobiles,
                "atUserIds":atUserIds,
                "isAtAll": isAtAll
            }
        }
        return self.send(data)
    
    def send_link(self,text,title,messageUrl,picUrl = ''):
        '''发送link类型消息

        Parameters
        -----------
        text:str
            消息内容。如果太长只会部分展示
        title:str   
            消息标题
        messageUrl:str  
            点击消息跳转的URL
        picUrl:str  
            图片URL
        
        Examples
        -----------
        >>> from datamation.send import dingtalk
        >>> ding = dingtalk.dingtalk('https://oapi.dingtalk.com/robot/send?access_token=xxx')
        >>> ding.send_link('测试','测试','https://www.baidu.com')
        '''
        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": picUrl,
                "messageUrl": messageUrl
            }
        }
        return self.send(data)
    
    def send_actionCard(self,title,text,btns,singleTitle = '',singleURL = '',btnOrientation = 0,hideAvatar = 0):
        '''发送actionCard类型消息

        Parameters
        -----------
        title:str
            首屏会话透出的展示内容
        text:str
            markdown格式的消息
        btns:list   
            按钮的信息：title-按钮方案，actionURL-点击按钮触发的URL
        singleTitle:str
            单个按钮的方案。(设置此项和singleURL后btns无效。) 
        singleURL:str   
            点击singleTitle按钮触发的URL
        btnOrientation:str  
            0-按钮竖直排列，1-按钮横向排列
        hideAvatar:str  
            0-正常发消息者头像,1-隐藏发消息者头像
        
        Examples
        ---------
        >>> from datamation.send import dingtalk
        >>> ding = dingtalk(url = 'https://oapi.dingtalk.com/robot/send?access_token=xxx')
        >>> btns = ['{"title":"内容不错","actionURL":"https://www.baidu.com"}','{"title":"不感兴趣","actionURL":"https://www.baidu.com"}']
        >>> ding.send_actionCard('测试','测试',btns)

        '''
        data = {
            "actionCard": {
                "title": title,
                "text": text,
                "btns": btns,
                "singleTitle": singleTitle,
                "singleURL": singleURL,
                "btnOrientation": btnOrientation,
                "hideAvatar": hideAvatar
            },
            "msgtype": "actionCard"
        }
        return self.send(data)

    def send(self,data):
        '''
        Parameters
        -----------
        data:dict

        Examples
        ---------
        text类型:
        {
            "at": {
                "atMobiles":[
                    "180xxxxxx"
                ],
                "atUserIds":[
                    "user123"
                ],
                "isAtAll": false
            },
            "text": {
                "content":"我就是我, @XXX 是不一样的烟火"
            },
            "msgtype":"text"
        }
        link类型:
        {
            "msgtype": "link", 
            "link": {
                "text": "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林", 
                "title": "时代的火车向前开", 
                "picUrl": "", 
                "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
            }
        }

        markdown类型
        {
             "msgtype": "markdown",
             "markdown": {
                 "title":"杭州天气",
                 "text": "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
             },
              "at": {
                  "atMobiles": [
                      "150XXXXXXXX"
                  ],
                  "atUserIds": [
                      "user123"
                  ],
                  "isAtAll": false
              }
         }


        '''
        url = self.url
        if self.__secret:
            url  = url+'&timestamp={}&sign={}'.format(*self.get_sign())
        res = requests.post(url,json = data)
        return res.json()

