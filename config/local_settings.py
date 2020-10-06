import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('E:\VoiceTestGame', 'db.sqlite3'),
    }
}
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voice_test_game',
        'PORT': 3306,
        "HOST": '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS': {
            'autocommit': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}'''
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voice_test_game',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'voice_test_game_database.Dijkstra.secoder.local',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}'''
