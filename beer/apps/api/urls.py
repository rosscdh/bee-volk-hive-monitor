# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

from beer.apps.monitor.api.views import (MonitorViewset,
                                         FetchUrlView)


router = routers.SimpleRouter(trailing_slash=False)

"""
Generic ViewSets
"""
router.register(r'monitor', MonitorViewset, base_name='monitor')

urlpatterns = patterns('',
                       # Custom Compound viewsets
                       url(r'url/check', FetchUrlView.as_view(), name='url_check'),
                       ) + router.urls
