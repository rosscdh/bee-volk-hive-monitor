from . import BASE_DIR
from ..local_settings import PROJECT_ENVIRONMENT
from ..local_settings import ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN

import os

#
# Custom url used in the api to prefix reverses as we dont have access to request object
#
BASE_URL = 'http://localhost:8000'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjcfpgezcvvksf5yl@zi=nfpmr_2*q251d9r=o#$0h9+frwivl'

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
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'beer.apps.api',
    'beer.apps.monitor',
    'beer.apps.phearjs',
)

HELPER_APPS = (
    'pipeline',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',

    'djcelery',
    'actstream',
    'djangobower',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS

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

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, '../', 'bower_components')
BOWER_PATH = '/usr/local/bin/bower'
BOWER_INSTALLED_APPS = (
    'angular-animate#1.3.8',
    'angular-cookies#1.3.4',
    'angular-touch#1.3.4',
    'angular-sanitize#1.3.4',
    'jquery#2.1.1',
    'angular-resource#1.3.4',
    'angular-ui-router#0.2.13',
    'bootstrap-sass-official#3.3.1',
    'angular-bootstrap#0.12.0',
    'modernizr#2.8.3',
    'satellizer#^0.9.2',
    'angular-breadcrumb#0.3.2',
    'angular-moment#0.9.0',
    'moment#2.9.0',
    'ngstorage#0.3.0',
    'angular-local-storage#0.1.5',
    'angular-scroll#0.6.5',
    'ngSticky#1.7.9',
    'angular-carousel#0.3.10',
    'angular-fontawesome#0.3.2',
    'angular-loading-bar#0.7.1',
    'angular-messages#1.4.0',
    'angular-validation-match#1.3.0',
    'angular-slugify#1.0.0',
    'ng-simplePagination#1.0.3',
    'angular-truncate',
    'ng-file-upload#3.1.0',
    'ng-file-upload-shim#3.1.0',
    'angular-intercom#2.0.4',
    'angular-mixpanel#1.1.0',
    'ngDialog#0.3',
    'angular-mailchimp#*',
    'allmighty-autocomplete#*',
    'v-accordion#1.2.3',
    'jquery-ui#1.11.4',
    'FitVids#1.1.0',
    'flexslider#2.5.0',
    'inview#*',
    'jquery-placeholder#2.1.2',
    'isMobile#0.3.6',
    'animate.css#3.3.0',
    'bootstrap-hover-dropdown#2.1.3'
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
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
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 5,
    'PAGINATE_BY': 15
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
