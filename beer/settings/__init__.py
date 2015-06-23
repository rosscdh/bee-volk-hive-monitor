"""
Django settings for m1_news project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_ENVIRONMENT = 'production'  # default to production but local_settings can override this

from .common_settings import *

IS_TESTING = False
for test_app in ['testserver', 'test', 'jenkins']:
    if test_app in sys.argv[1:2]:
        IS_TESTING = True

#
# Loaded form the dir above settings/*
#
try:
    from ..local_settings import *
    from .logging_settings import *
except ImportError:
    # no local_settings.py found
    from .logging_settings import *


if IS_TESTING:
    try:
        from .test_settings import *
    except ImportError:
        print("Could not load test_settings")
