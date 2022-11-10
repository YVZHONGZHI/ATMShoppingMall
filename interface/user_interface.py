# interface放逻辑接口层
# user_interface.py放用户接口

from db import db_handle
from lib import common


# 根据不同的接口类型传入不同的日志对象
user_logger = common.get_logger(log_type='user')


# 注册接口
# 接受src.py用户视图层传过来的username和password
def register_interface(username, password, balance=15000):
    # 把username传给db_handler.py数据处理层后结果返回user_dic
    user_dic = db_handle.select(username)

    # 根据user_dic判断
    if user_dic:
        # 把结果传给src.py用户视图层
        return False, f'用户名[{username}]已存在!'

    # 调common.py的密码加密
    password = common.get_pwd_md5(password)

    user_dic = {
        'username':username,
        'password':password,
        'balance':balance,
        'flow':[],
        'shop_car':{},
        'locked':False
    }

    # 根据user_dic判断
    # 把结果传给db_handler.py数据处理层
    db_handle.save(user_dic)
    msg = f'{username} 注册成功!'
    # 把结果传给src.py用户视图层
    user_logger.info(msg)
    return True, msg


# 登录接口
def login_interface(username, password):
    user_dic = db_handle.select(username)

    if user_dic:

        if user_dic.get('locked'):
            return False, '当前用户已被锁定'

        password = common.get_pwd_md5(password)

        if password == user_dic.get('password'):
            msg = f'用户:[{username}] 登录成功!'
            user_logger.info(msg)
            return True, msg

        else:
            msg = f'用户:[{username}] 密码错误!'
            user_logger.warn(msg)
            return False, msg

    msg = f'用户:[{username}] 用户不存在,请重新输入!'
    return False, msg


# 查看余额接口
def check_bal_interface(username):
    user_dic = db_handle.select(username)
    return user_dic['balance']