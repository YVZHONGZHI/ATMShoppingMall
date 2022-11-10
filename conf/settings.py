# conf放配置文件(日志的路径,数据库的路径)
# 不要去导入core的东西
# 获取项目根路径
# 获取user_data文件夹路径

import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USER_DATA_PATH = os.path.join(BASE_DIR,'db','user_data')


# 日志
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
logfile_dir = os.path.join(BASE_PATH, 'log')

logfile_name = 'user.log'

if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

logfile_path = os.path.join(logfile_dir, logfile_name)

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logfile_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}