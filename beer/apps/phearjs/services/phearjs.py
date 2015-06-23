# -*- coding: utf-8 -*-
from django.conf import settings

import requests


class RequestException(Exception):
    pass


class PhearJsService(object):
    """
    Service to communicate with the phearjs resorce collector
    """
    def __init__(self, url, **kwargs):
        self.url = url
        self.PHEARJS_URL = kwargs.get('PHEARJS_URL',
                                      getattr(settings,
                                              'PHEARJS_URL',
                                              'http://localhost:8183')
                                      )

    def process(self, **kwargs):

        params = {
            'fetch_url': self.url
        }
        params.update(kwargs)

        # try:
        resp = requests.get(self.PHEARJS_URL, params=params)

        if str(resp.status_code)[0:1] not in ['2']:
            raise RequestException('Error ocurred in request: %s - %s' % (self.PHEARJS_URL, resp.content))

        return resp

        # except Exception as e:
        #     raise RequestException(unicode(e))
