# -*- coding: utf-8 -*-
from django.utils import encoding

from urlparse import urlparse

from beer.apps.phearjs.services import PhearJsService

from ..models import (Url,
                      UrlLog)

import hashlib


class FetchUrlService(object):
    """
    Service accepts url object and checks to see if it exists
    if not creates a new one and setups the Url object data
    associates the url object with provided MonitorSite object
    """
    def __init__(self, url, monitor_site=None, **kwargs):
        # convert the url string into a url object
        self.url, self.url_is_new = self.get_url_object(url_string=url)

        if 1 or self.url_is_new is True:
            parsed_url = urlparse(self.url.url)
            self.url.scheme = parsed_url.scheme
            self.url.netloc = parsed_url.netloc
            self.url.path = parsed_url.path
            self.url.params = parsed_url.params
            self.url.query = parsed_url.query
            self.url.fragment = parsed_url.fragment
            self.url.save(update_fields=['scheme', 'netloc', 'path', 'params', 'query', 'fragment'])

        self.monitor_site = monitor_site

    def get_url_object(self, url_string):
        return Url.objects.get_or_create(url=url_string)

    def process_url_object(self, url):
        s = PhearJsService(url=url.url)
        self.log_url_response(resp=s.process())

    def log_url_response(self, resp):
        self.url_log, self.url_log_is_new = self.calculate_url_response_crc(resp_data=resp.json())

    def calculate_url_response_crc(self, resp_data):
        content = resp_data.get('content')
        digest = hashlib.sha256(content.encode('utf-8')).hexdigest()
        url_log, is_new = UrlLog.objects.get_or_create(digest=digest, url=self.url)

        # Update the log data only if it is new§
        if is_new is True:
            url_log.data = resp_data
            url_log.save(update_fields=['data'])

        return url_log, is_new

    def process(self, **kwargs):
        # params = {}
        # params.update(kwargs)

        self.process_url_object(url=self.url)

        return {'url': {'object': self.url,
                        'is_new': self.url_is_new},
                'log': {'object': self.url_log,
                        'is_new': self.url_log_is_new}
                }
