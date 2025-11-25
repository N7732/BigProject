from .Base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development-specific settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}