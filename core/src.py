# core放用户视图层
# core放核心代码

from interface import bank_interface
from interface import shop_interface
from interface import user_interface
from lib import common


login_user = None

# 注册功能
def register():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()

        if password == re_password:
            flag, msg = user_interface.register_interface(username, password)

            if flag:
                print(msg)
                break

            else:
                print(msg)

        else:
            print('两次密码不一致,请重新注册')


# 登录功能
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()

        flag, msg = user_interface.login_interface(username, password)

        if flag:
            print(msg)
            global login_user
            login_user = username
            break

        else:
            print(msg)


# 查询余额
@common.login_auth
def check_balance():
    balance = user_interface.check_bal_interface(login_user)

    print(f'用户{login_user}账户余额为:{balance}')


# 取款功能
@common.login_auth
def withdraw():
    while True:
        input_money = input('请输入取款金额:').strip()

        if not input_money.isdigit():
            print('请重新输入')
            continue

        flag, msg = bank_interface.withdraw_interface(login_user, input_money)

        if flag:
            print(msg)
            break

        else:
            print(msg)


# 还款功能
@common.login_auth
def repay():
    while True:
        input_money = input('请输入需要还款的金额:').strip()

        if not input_money.isdigit():
            print('请输入正确的金额')
            continue
        input_money = int(input_money)

        if input_money > 0:
            flag, msg = bank_interface.repay_interface(login_user, input_money)

            if flag:
                print(msg)
                break
        else:
            print('输入的金额不能小于0')


# 转账功能
@common.login_auth
def transfer():
    while True:
        to_user = input('请输入转账目标用户:').strip()
        money = input('请输入转账金额:').strip()

        if not money.isdigit():
            print('请输入正确的金额!')
            continue

        money = int(money)

        if money > 0:
            flag, msg = bank_interface.transfer_interface(login_user, to_user, money)

            if flag:
                print(msg)
                break
            else:
                print(msg)

        else:
            print('请输入正确的金额!')


# 查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(login_user)

    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户没有流水!')


# 购物功能
@common.login_auth
def shopping():
    shop_list = [
        ['商品1', 30],
        ['商品2', 250],
        ['商品3', 28],
        ['商品4', 15],
        ['商品5', 100000],
        ['商品6', 20000],
    ]

    shopping_car = {}

    while True:
        print('===========================================')
        # 枚举
        for index, shop in enumerate(shop_list):
            shop_name, shop_price = shop
            print(f'商品编号为:[{index}]',f'商品名称:[{shop_name}]',f'商品单价:[{shop_price}]')
        print('===========================================')

        choice = input('请输入商品编号 (是否结账输入y or n):').strip()

        if choice == 'y':
            if not shopping_car:
                print('购物车是空的,不能支付,请重新输入!')
                continue

            flag, msg = shop_interface.shopping_interface(login_user, shopping_car)

            if flag:
                print(msg)
                break

            else:
                print(msg)

        elif choice == 'n':
            if not shopping_car:
                print('购物车是空的,不能增加,请重新输入!')
                continue

            flag, msg = shop_interface.add_shop_car_interface(login_user, shopping_car)

            if flag:
                print(msg)
                break

        if not choice.isdigit():
            print('商品编号非数字,请重输')
            continue

        choice = int(choice)

        if choice not in range(len(shop_list)):
            print('请输入给定的商品编号!')
            continue

        shop_name, shop_price = shop_list[choice]

        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1

        else:
            shopping_car[shop_name] = [shop_price, 1]

        print('当前购物车:', shopping_car)


# 查看购物车
@common.login_auth
def check_shop_car():
    shop_car = shop_interface.check_shop_car_interface(login_user)
    print(shop_car)


# 管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.admin_run()


func_dic = {
    '0': ['退出', None],
    '1': ['注册', register],
    '2': ['登录', login],
    '3': ['查询余额', check_balance],
    '4': ['取款', withdraw],
    '5': ['还款', repay],
    '6': ['转账', transfer],
    '7': ['查看流水', check_flow],
    '8': ['购物', shopping],
    '9': ['查看购物车', check_shop_car],
    '10': ['管理员功能', admin]
}


def run():
    while True:
        print('===========================================')
        for w in func_dic:
            print('               ', ".".join([w, func_dic[w][0]]))
        print('===========================================')

        choice = input('请输入功能编号:').strip()
        if not choice.isdigit():
            print('功能编号非数字,请重输')
            continue

        if choice == '0':
            break

        if choice in func_dic:
            func_dic[choice][1]()

        else:
            print('请输入给定的功能编号!')