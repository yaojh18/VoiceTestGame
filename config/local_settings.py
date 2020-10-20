import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
    }
}

WEAPP_ID = 'wxcec8955125bd6732'
WEAPP_SECRETE = 'd26321578e183029be05d63ac982a660'
