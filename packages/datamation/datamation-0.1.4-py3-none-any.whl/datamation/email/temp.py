import requests

from datamation import log

logger = log.get_logger()

class temp_mail(object):
    def __init__(self,name=''):
        '''临时邮箱'''
        try:
            self.session = requests.Session()
            self.session.get('http://24mail.chacuo.net/')
            self._mail = lambda :self.session.post('http://24mail.chacuo.net/',data = {'data':'abcd','type':'refresh','arg':''})
        
            if name and self.replace(name):
                self._name = self.email
            else:
                if name:
                    logger.error('指定失败 生成随机邮箱 需要继续尝试请使用replace方法~')
                self._name = self._mail().json()['data'][0].get('user').get('USER')
                self.email = f"{self._name}@chacuo.net"
            logger.info(' 邮箱获取成功：'+self.email)

        except Exception as e:
            logger.exception('this is an exception message')
        
    def reset_name(self,name=''):
        '''更换邮箱 输入参数为空则随机生成'''
        if name:
            data = {'data':name,'type':'set','arg':'d=chacuo.net_f='}
        else:
            data = {'data':name,'type':'renew','arg':'d=chacuo.net_f='}
            
        html = self.session.post('http://24mail.chacuo.net/',data = data)
        if html.json()['data'][0]:
            self.email = f"{html.json()['data'][0]}@chacuo.net"
            return True
        else:
            return False
        
    def get(self,mid = ''):
        '''获取邮件 mid参数为空则返回邮件列表 指定mid则返回对应邮件内容'''
        if mid:
            data = {'data':self._name,
                    'type': 'mailinfo',
                    'arg': 'f=' + str(mid)}
            return self.session.post('http://24mail.chacuo.net/', data=data).json()
        else:
            return self._mail().json().get('data')[0].get('list')
        