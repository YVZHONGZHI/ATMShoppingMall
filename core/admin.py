# core放用户视图层
# core放核心代码

from core import src
from interface import admin_interface


# 增加账户
def add_user():
    src.register()


# 修改额度
def change_balance():
    while True:
        change_user = input('请输入需要修改额度的用户:').strip()

        money = input('请输入需要修改的用户额度:').strip()
        if not money.isdigit():
            continue

        flag, msg = admin_interface.change_balance_interface(change_user, money)

        if flag:
            print(msg)
            break
        else:
            print(msg)


# 冻结账户
def lock_user():
    while True:
        change_user = input('请输入需要冻结账户的用户:').strip()
        flag, msg = admin_interface.lock_user_interface(change_user)

        if flag:
            print(msg)
            break
        else:
            print(msg)


# 管理员功能字典
admin_func = {
    '0': ['退出管理员功能', None],
    '1': ['增加账户', add_user],
    '2': ['修改额度', change_balance],
    '3': ['冻结账户', lock_user]
}


def admin_run():
    while True:
        print('===========================================')
        for w in admin_func:
            print('               ', ".".join([w, admin_func[w][0]]))
        print('===========================================')

        choice = input('请输入管理员功能编号:').strip()
        if not choice.isdigit():
            print('功能编号非数字,请重输')
            continue

        if choice == '0':
            break

        if choice in admin_func:
            admin_func[choice][1]()

        else:
            print('请输入给定的功能编号!')