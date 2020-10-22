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
WEAPP_ID = 'wxcec8955125bd6732'
WEAPP_SECRETE = 'd26321578e183029be05d63ac982a660'
