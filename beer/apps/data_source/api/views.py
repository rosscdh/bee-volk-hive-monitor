# -*- coding: utf-8 -*-
from rest_framework import viewsets
#from rest_framework.response import Response

from social.apps.django_app.default.models import UserSocialAuth

from ..models import DataSource
from .serializers import DataSourceSerializer, UserSocialAuthSerializer

import logging
logger = logging.getLogger('django.request')


class UserSocialAuthViewSet(viewsets.ModelViewSet):
    model = UserSocialAuth
    serializer_class = UserSocialAuthSerializer
    queryset = UserSocialAuth.objects.all()


class DataSourceViewSet(viewsets.ModelViewSet):
    model = DataSource
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()
