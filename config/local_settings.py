import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
    }
}

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voice_test_game',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}'''
WEAPP_URL = 'https://api.weixin.qq.com/sns/jscode2session'
WEAPP_ID = 'wxcec8955125bd6732'
WEAPP_SECRETE = 'd26321578e183029be05d63ac982a660'

APP_URL = 'http://zentao.c-smb.com:23101'
APP_ID = '13001000002000000000010'
APP_SECRET = '260542ef8e56432d88d179400a73edf9'
