# -*- coding: utf-8 -*-
from . import BASE_DIR
from ..local_settings import PROJECT_ENVIRONMENT


#
# Development
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    'handlers': {
        "rq_console": {
            "level": "DEBUG",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        "rq.worker": {
            "handlers": ["rq_console", "console"],
            "level": "DEBUG"
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}


if PROJECT_ENVIRONMENT in ['staging', 'production']:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'papertrail_format': {
                'format': '%(asctime)s [%(levelname)s] [%(filename)s->%(funcName)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            "rq_console": {
                "format": "%(asctime)s %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        'handlers': {
            'papertrail_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.SysLogHandler',
                'address': ('logs2.papertrailapp.com', 29549),
                'formatter': 'papertrail_format',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'papertrail_format',
            },
            "rq_console": {
                "level": "DEBUG",
                "class": "rq.utils.ColorizingStreamHandler",
                "formatter": "rq_console",
                "exclude": ["%(asctime)s"],
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['papertrail_handler'],
                'level': 'INFO',
            },
            "rq.worker": {
                "handlers": ["papertrail_handler"],
                "level": "DEBUG"
            },
        }
    }
