# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True

from . import BASE_DIR

import os
import logging

logging.disable(logging.CRITICAL)

DEBUG = False  # msut be set to false to emulate production


PROJECT_ENVIRONMENT = 'test'

ATOMIC_REQUESTS = True

DEFAULT_KEY_UUID = "c83e21df7b6e437b89a22fa923d5bd3f"

#
# For the moment we use sqlite3 for testing as we are not doign anything postgres specific
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.db'),
    }
}

# extra settings for only test
# INSTALLED_APPS = INSTALLED_APPS + (
#     #'casper',
#     #'colortools',
#     # Lawpal modules
# )

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

# faster passwords but far less secure in test
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

PROCESS_IMAGES_ASYNC = False

STATIC_URL = '/static/'
STATIC_ROOT = '../static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '../media/'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
