# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from beer.apps.box.api.views import (BoxViewSet,
                                     BoxRegistrationEndpoint,
                                     BoxPusherPresenceAuthEndpoint,)
from beer.apps.hive.api.views import HiveViewSet

router = routers.SimpleRouter(trailing_slash=True)

#
# Generic ViewSets
#

router.register(r'boxes', BoxViewSet)
router.register(r'hives', HiveViewSet)

#
# Standard URLS
#
urlpatterns = patterns('',
                       # Hives

                       # Sensors

                       # Boxes - Gen 1
                       url(r'^box/register/$', csrf_exempt(BoxRegistrationEndpoint.as_view()), name='box_registration'),
                       url(r'^box/auth/pusher/$', csrf_exempt(BoxPusherPresenceAuthEndpoint.as_view()), name='pusher_auth'),

                       # Events
                       url(r'^', include('beer.apps.evt.urls', namespace='evt')),
                       ) + router.urls
