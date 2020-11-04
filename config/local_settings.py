import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
    }
}

WEAPP_ID = 'wxcec8955125bd6732'
WEAPP_SECRETE = 'd26321578e183029be05d63ac982a660'

APP_URL = 'http://zentao.c-smb.com:23101'
APP_ID = '13001000002000000000010'
APP_SECRET = '260542ef8e56432d88d179400a73edf9'
