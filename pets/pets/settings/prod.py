from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASENAME', 'cademeubicho'),
        'USER': os.environ.get('DATABASEUSER', 'django'),
        'PASSWORD': os.environ.get('DATABASEPASSWORD', 'django'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}