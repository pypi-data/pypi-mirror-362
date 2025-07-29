

import re

def etk_email_addr(txt):
    '''邮件地址提取
    
    Parameters
    -----------
    txt : str
        文本字符串

    Returns
    --------
    list
        解析后的邮箱列表
    '''
    mail_re =  r'\w*@[0-9a-zA-Z]{\w}\.{1,3}'
    return list(set(re.findall(mail_re,''.join(txt))))

