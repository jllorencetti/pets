# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from decouple import config, Csv
from dj_database_url import parse as db_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1',
)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTS_APPS = (
    'easy_thumbnails',
    'braces',
    'crispy_forms',
    'social.apps.django_app.default',
    'opbeat.contrib.django',
    'compressor',
    'password_reset',
    'rest_framework',
    'corsheaders',
)

PROJECT_APPS = (
    'users',
    'meupet',
    'common',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTS_APPS

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.Facebook2OAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'users.pipeline.add_facebook_link',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

ROOT_URLCONF = 'pets.urls'

WSGI_APPLICATION = 'pets.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

conn_max_age = config('DB_CONN_MAX_AGE', default=0, cast=int)
default_db_url = config('DATABASE_URL')
DATABASES = {
    'default': db_url(default_db_url, conn_max_age=conn_max_age)
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# Setting static folder for site-wide files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

# static root folder, where static files will be collected to
STATIC_ROOT = os.path.join(BASE_DIR, '../../static_root')

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
]

COMPRESS_OFFLINE = True

# Setting media configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')

# Setting easy_thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'pet_thumb': {'size': (350, 350), 'crop': True, 'upscale': True},
        'pet_poster': {'size': (550, 550), 'crop': True, 'upscale': True},
    }
}

THUMBNAIL_BASEDIR = 'pet_thumbs'

LOGIN_URL = 'users:login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTH_USER_MODEL = 'users.OwnerProfile'

# Authentication
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'users:confirm_information'

SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY', default='')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET', default='')

SOCIAL_AUTH_TWITTER_KEY = config('SOCIAL_AUTH_TWITTER_KEY', default='')
SOCIAL_AUTH_TWITTER_SECRET = config('SOCIAL_AUTH_TWITTER_SECRET', default='')

FACEBOOK_SHARE_URL = 'https://www.facebook.com/sharer.php?u=http://cademeubicho.com/pets/{}/'
TWITTER_SHARE_URL = 'https://twitter.com/share?url=http://cademeubicho.com/pets/{}/'

OPBEAT = {
    'ORGANIZATION_ID': config('OPBEAT_ORGANIZATION_ID', default=''),
    'APP_ID': config('OPBEAT_APP_ID', default=''),
    'SECRET_TOKEN': config('OPBEAT_SECRET_TOKEN', default=''),
}

default_email_backend = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_BACKEND = config('EMAIL_BACKEND', default=default_email_backend)
EMAIL_HOST = config('EMAIL_HOST', default='example.com')
EMAIL_PORT = config('EMAIL_PORT', default='0')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='dummy@example.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='example')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='dummy@example.com')

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
