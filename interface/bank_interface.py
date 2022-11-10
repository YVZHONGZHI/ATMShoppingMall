# interface放逻辑接口层
# bank_interface.py放银行相关业务的接口

from db import db_handle
from lib import common


# 根据不同的接口类型传入不同的日志对象
bank_logger = common.get_logger(log_type='bank')


# 提现接口
def withdraw_interface(username, money):
    user_dic = db_handle.select(username)
    balance = int(user_dic.get('balance'))
    money2 = int(money) * 1.05

    if balance >= money2:
        balance -= money2
        user_dic['balance'] = balance

        flow = f'用户[{username}]提现金额[{money}w]成功,手续费为:[{money2 - float(money)}w]'
        user_dic['flow'].append(flow)

        db_handle.save(user_dic)
        bank_logger.info(flow)

        return True, flow

    return False, '提现金额不足,请重新输入!'


# 还款接口
def repay_interface(username, money):
    user_dic = db_handle.select(username)
    user_dic['balance'] += money
    flow = f'用户:[{username}] 还款:[{money}w] 成功!'
    user_dic['flow'].append(flow)
    db_handle.save(user_dic)
    return True, flow


# 转账接口
def transfer_interface(login_user, to_user, money):
    login_user_dic = db_handle.select(login_user)
    to_user_dic = db_handle.select(to_user)

    if not to_user_dic:
        return False, '目标用户不存在'

    if login_user_dic['balance'] >= money:
        login_user_dic['balance'] -= money
        to_user_dic['balance'] += money
        login_user_flow = f'用户:[{login_user}] 给用户:[{to_user}] 转账:[{money}w] 成功!'
        login_user_dic['flow'].append(login_user_flow)
        to_user_flow = f'用户:[{to_user}] 接收用户:[{login_user}] 转账:[{money}w] 成功!'
        to_user_dic['flow'].append(to_user_flow)
        db_handle.save(login_user_dic)
        db_handle.save(to_user_dic)
        return True,login_user_flow
    return False,'当前用户转账金额不足!'


# 查看流水接口
def check_flow_interface(login_user):
    user_dic = db_handle.select(login_user)
    return user_dic.get('flow')


# 支付接口
def pay_interface(login_user, cost):
    user_dic = db_handle.select(login_user)

    if user_dic.get('balance') >= cost:
        user_dic['balance'] -= cost
        flow = f'用户消费金额:[{cost}w]'
        user_dic['flow'].append(flow)
        db_handle.save(user_dic)
        return True
    return False