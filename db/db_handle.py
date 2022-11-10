# db放数据处理层
# db放数据库功能(读写功能)

import json
import os
from conf import settings


# 保存数据
def save(user_dic):
    username = user_dic.get('username')
    user_path = os.path.join(settings.USER_DATA_PATH, f'{username}.json')

    with open(user_path, 'w', encoding='utf-8') as w:
        json.dump(user_dic, w, ensure_ascii=False)


# 查看数据
def select(username):
    user_path = os.path.join(settings.USER_DATA_PATH, f'{username}.json')

    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8') as w:
            user_dic = json.load(w)
            return user_dic