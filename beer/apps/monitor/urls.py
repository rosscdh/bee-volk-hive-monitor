# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from .views import UrlHistoryView

urlpatterns = patterns('',
                       # Custom Compound viewsets
                        url(r'url/(?P<pk>\d+)/history', UrlHistoryView.as_view(), name='url_history'),
                       )
