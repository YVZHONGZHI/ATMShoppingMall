# lib放配置信息
# lib放常用的模块,包

import hashlib
import logging.config
from conf import settings


# md5 加密
def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = '加盐'
    md5_obj.update(salt.encode('utf-8'))
    return md5_obj.hexdigest()


# 登录认证无参装饰器
def login_auth(func):
    from core import src

    def ineer(*args, **kwargs):
        if src.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('未出示证明,无法执行功能服务!')
            src.login()
    return ineer


# 增加日志功能
def get_logger(log_type):
    logging.config.dictConfig(settings.LOGGING_DIC)
    logger = logging.getLogger(log_type)
    return logger