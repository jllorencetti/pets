# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ca#j$qam2uh*))o*1&31(_7ud1k6hrjwn+5gd9qf2g1ukv2td1')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1',
)

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*')]

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
)

PROJECT_APPS = (
    'users',
    'meupet',
    'common'
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTS_APPS

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', os.path.join(BASE_DIR, '../db.sqlite3')),
        'USER': os.environ.get('DB_USERNAME', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_IP', ''),
        'PORT': os.environ.get('DB_PORT', ''),
        'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', 0)),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

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

# Setting media configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')

# Setting easy_thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'pet_thumb': {'size': (350, 350), 'crop': True, 'upscale': True},
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

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')

OPBEAT = {
    'ORGANIZATION_ID': os.environ.get('OPBEAT_ORGANIZATION_ID'),
    'APP_ID': os.environ.get('OPBEAT_APP_ID'),
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN'),
}
