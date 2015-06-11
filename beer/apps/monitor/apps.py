# -*- coding: utf-8 -*-
from django.apps import AppConfig
from actstream import registry


class MonitorAppConfig(AppConfig):
    name = 'beer.apps.monitor'

    def ready(self):
        registry.register(self.get_model('Url'))
        registry.register(self.get_model('UrlLog'))
