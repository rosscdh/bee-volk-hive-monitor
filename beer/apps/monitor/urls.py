# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from .views import UrlHistoryView, ThambnailView

urlpatterns = patterns('',
                       # Custom Compound viewsets
                       url(r'url/(?P<pk>\d+)/history', UrlHistoryView.as_view(), name='url_history'),
                       url(r'url/log/(?P<pk>\d+)/thumb(?:/(?P<w>[\d]+)x(?P<h>[\d]+)/)?', ThambnailView.as_view(), name='url_log_thumbnail'),
                       )
