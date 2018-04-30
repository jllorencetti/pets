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
DEBUG = config('DEBUG', default=False, cast=bool)

INTERNAL_IPS = config('INTERNAL_IPS', default='', cast=Csv())

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
)

THIRD_PARTS_APPS = (
    'compressor',
    'corsheaders',
    'crispy_forms',
    'easy_thumbnails',
    'opbeat.contrib.django',
    'password_reset',
    'rest_framework',
    'social_django',
)

PROJECT_APPS = (
    'cities',
    'common',
    'meupet',
    'users',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTS_APPS

SITE_ID = 1

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

PROJECT_TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'meupet.context_processors.pets_count',
                'meupet.context_processors.sidemenu',
                'users.context_processors.users_count',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', PROJECT_TEMPLATE_LOADERS),
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'users.pipeline.add_facebook_link',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
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

LANGUAGE_CODE = 'pt-BR'

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
default_static_root = os.path.join(BASE_DIR, '../../static_root')
STATIC_ROOT = config('STATIC_ROOT', default=default_static_root)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, '../locale')
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
]

COMPRESS_OFFLINE = True

# Setting media configuration
MEDIA_URL = '/media/'
default_media_root = os.path.join(BASE_DIR, '../../media')
MEDIA_ROOT = config('MEDIA_ROOT', default=default_media_root)

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

CITIES_DATA_LOCATION = os.path.join(BASE_DIR, '../../data/cities_data')

# Authentication
LOGIN_REDIRECT_URL = 'meupet:index'
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'users:confirm_information'

SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]

# Number of days used to consider a register staled
DAYS_TO_STALE_REGISTER = config('DAYS_TO_STALE_REGISTER', default=90, cast=int)

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

SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='dummy@example.com')

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
