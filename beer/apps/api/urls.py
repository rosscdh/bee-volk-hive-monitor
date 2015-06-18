# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

from beer.apps.monitor.api.views import (MonitorViewset,
                                         UrlViewset,
                                         UrlLogViewset,
                                         FetchUrlView,
                                         DiffUrlView)

from beer.apps.monitor.views import (UrlLogScreenshotView, UrlLogScreenshotCompareView,)

router = routers.SimpleRouter(trailing_slash=False)

"""
Generic ViewSets
"""
router.register(r'monitor', MonitorViewset, base_name='monitor')
router.register(r'url', UrlViewset, base_name='url')
router.register(r'log', UrlLogViewset, base_name='log')


urlpatterns = patterns('',
                       # Custom Compound viewsets
                       url(r'url/check', FetchUrlView.as_view(), name='url_check'),
                       url(r'url/(?P<a_pk>\d+)/(?P<b_pk>\d+)/diff', DiffUrlView.as_view(), name='url_diff'),
                       url(r'url/(?P<pk>\d+)/screenshot', UrlLogScreenshotView.as_view(), name='url_screenshot'),
                       url(r'url/(?P<pk>\d+)/(?P<pk_b>\d+)/compare', UrlLogScreenshotCompareView.as_view(), name='url_compare'),
                       ) + router.urls
