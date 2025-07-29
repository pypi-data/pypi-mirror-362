
import logging
import io
import datetime as dt 

_logs = {}
def get_logger(name='datamation',stdout=True,strio = None,file_out= False):   
    logger= logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s',datefmt ='%Y-%m-%d %H:%M:%S ')
       
    logger.handlers.clear()
    if stdout:
        # 控制台
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.DEBUG)
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)

    # 文件
    if file_out:
        fh_all = logging.FileHandler(f"log\{dt.datetime.now().date().strftime('%Y%m%d')}.log")
        fh_all.setLevel(logging.DEBUG)
        fh_all.setFormatter(formatter)
        logger.addHandler(fh_all)

    if strio:
        # 保存为字符串
        _logs[name]= io.StringIO()
        log_str = logging.StreamHandler(_logs[name])
        log_str.setLevel(logging.DEBUG)
        log_str.setFormatter(formatter)
        logger.addHandler(log_str)
    return logger
