# -*- coding: UTF-8 -*-
from . import BASE_DIR
from ..local_settings import PROJECT_ENVIRONMENT
from ..local_settings import ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN

import os
import datetime

DJANGO_ENV = os.getenv('DJANGO_ENV', os.getenv('RAILS_ENV', 'development'))

SITE_ID = 1

#
# Custom url used in the api to prefix reverses as we dont have access to request object
#
BASE_URL = 'http://localhost:8000'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjcfpgezcvvksf5yl@zi=nfpmr_2*q251d9r=o#$0h9+frwivl'
URL_ENCODE_SECRET_KEY = '^@+2#(=7oa3_d29zl=9sn!zehf6at*9=wrkli3+y03lc*qhl@4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'beer.apps.public',

    'beer.apps.api',

    'beer.apps.payment_plans',
    'beer.apps.role_permission',

    'beer.apps.box',
    'beer.apps.sensor',
    'beer.apps.evt',

    'beer.apps.hive',

    'beer.apps.client',
    'beer.apps.project',
)

HELPER_APPS = (
    'pipeline',
    'corsheaders',
    'django_extensions',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',

    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'pinax.eventlog',

    'geoposition',

    'pinax.stripe',

    'rulez',
    'django_rq',

#    'actstream',
    'easy_thumbnails',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # must come last
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'djangobower.finders.BowerFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../', 'media')
MEDIA_URL = '/media/'

ROOT_URLCONF = 'beer.urls'

WSGI_APPLICATION = 'beer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROLLBAR = {
    'access_token': ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN,
    'environment': PROJECT_ENVIRONMENT,
    'branch': 'master',
    'root': BASE_DIR,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('*',)
# CORS_ALLOW_HEADERS = (
#     'x-requested-with',
#     'content-type',
#     'accept',
#     'origin',
#     'authorization',
#     'x-csrftoken'
# )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        #'beer.apps.api.permissions.ApiObjectPermission',
    ),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 5,
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ALLOW_REFRESH': False,
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_LEEWAY': 300,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}


PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = 'cssmin'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS = {
    # 'pages': {
    #     'source_filenames': (
    #         'css/main.css',
    #     ),
    #     'output_filename': 'dist/pages.css',
    # }
}

PIPELINE_JS = {
    # 'pages': {
    #     'source_filenames': (
    #         'js/main.js',
    #     ),
    #     'output_filename': 'dist/pages.js',
    # }
}


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    'rulez.backends.ObjectPermissionBackend',
)

# All Auth /rest-auth config
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

PUSHER_APP_ID = 79947
PUSHER_KEY = 'cf7fc048e21bd39e6f82'
PUSHER_SECRET = '01d612aade08edc9dfde'

AWS_ACCESS_KEY_ID = 'AKIAIF76J6YUAN4UTFIA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'dev-hiveempire'

INFLUX_DB = {
    'host': os.getenv('INFLUX_DB_HOST', '192.168.99.100'),
    'port': os.getenv('INFLUX_DB_PORT', '32792'),
    'username': os.getenv('INFLUX_DB_USERNAME', 'root'),
    'password': os.getenv('INFLUX_DB_PASSWORD', 'root'),
    'database': os.getenv('INFLUX_DB_DATABASE', 'beekeep'),
}


PINAX_STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "your test public key")
PINAX_STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "your test secret key")

PAYMENTS_PLANS = {
    "early-bird-monthly": {
        "stripe_plan_id": "early-bird-monthly",
        "name": "Early Bird",
        "description": "Signup for the HiveEmpire Early Bird plan and save!<br /> Available for a limited time only.",
        "features": "Priority Support<br/>No long-term commitment",
        "price": 12,
        "currency": "euro",
        "interval": "month"
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 5,
        'DEFAULT_TIMEOUT': 360,
    },
}

try:
    env_path = os.path.join(BASE_DIR, 'config/environments/{DJANGO_ENV}/beer/local_settings.py'.format(DJANGO_ENV=DJANGO_ENV))
    environment_settings = open(env_path)
    exec(environment_settings)
except Exception as e:
    pass

try:
    from .local_settings import *
except:
    pass
