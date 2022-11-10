# interface放逻辑接口层
# shop_interface.py放购物商城接口

from db import db_handle
from lib import common


# 根据不同的接口类型传入不同的日志对象
shop_logger = common.get_logger(log_type='shop')


# 商品准备结算接口
def shopping_interface(login_user, shopping_car):
    cost = 0
    for price_number in shopping_car.values():
        price, number = price_number
        cost += (price * number)

    from interface import bank_interface

    flag = bank_interface.pay_interface(login_user, cost)

    if flag:
        msg = f'用户:[{login_user}]支付[{cost}w]成功,准备发货!'
        shop_logger.info(msg)
        return True, msg

    return False, '支付失败,金额不足'


# 购物车增加接口
def add_shop_car_interface(login_user, shopping_car):
    user_dic = db_handle.select(login_user)
    shop_car = user_dic.get('shop_car')
    for shop_name, price_number in shopping_car.items():
        number = price_number[1]

        if shop_name in shop_car:
            user_dic['shop_car'][shop_name][1] += number

        else:
            user_dic['shop_car'].update({shop_name:price_number})
    db_handle.save(user_dic)
    return True,'增加购物车成功!'


# 查看购物车接口
def check_shop_car_interface(username):
    user_dic = db_handle.select(username)
    return user_dic.get('shop_car')