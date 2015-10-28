# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

from .api.views import EventCreate


router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = patterns('',
  url(r'^event/$', EventCreate.as_view(), name='event-create'),
)
