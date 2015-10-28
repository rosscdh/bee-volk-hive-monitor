# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from beer.apps.stream.api.views import StreamViewSet
from beer.apps.data_source.api.views import DataSourceViewSet
from beer.apps.box.api.views import (BoxRegistrationEndpoint,
                                     BoxPusherPresenceAuthEndpoint,
                                     BoxViewSet,)
from beer.apps.me.api.views import (MeView,
                                    ChangePasswordView,
                                    RegisterView,
                                    VerifyUserView,
                                    ForgotPasswordView)

router = routers.SimpleRouter(trailing_slash=False)

"""
Generic ViewSets
"""
router.register(r'box', BoxViewSet)

router.register(r'data-streams', StreamViewSet, base_name='data-streams')
router.register(r'data-sources', DataSourceViewSet, base_name='data-sources')


urlpatterns = patterns('',
                       # User
                       url(r'^auth/jwt/refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),

                       # Register
                       url(r'^auth/register/$', RegisterView.as_view(), name='register'),
                       url(r'^auth/verify/$', VerifyUserView.as_view(), name='verify'),
                       url(r'^auth/forgot-password/$', ForgotPasswordView.as_view(), name='forgot_password'),

                       # Current user
                       url(r'^me/change-password', ChangePasswordView.as_view(), name='change-password'),
                       url(r'^me/$', MeView.as_view(), name='me'),

                       # Boxes
                       url(r'^box/register/$', csrf_exempt(BoxRegistrationEndpoint.as_view()), name='box_registration'),
                       url(r'^box/auth/pusher/$', csrf_exempt(BoxPusherPresenceAuthEndpoint.as_view()), name='pusher_auth'),

                       # Events
                       url(r'^', include('beer.apps.evt.urls', namespace='evt')),
                       ) + router.urls
