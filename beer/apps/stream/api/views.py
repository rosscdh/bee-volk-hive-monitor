# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from ..models import Stream
from .serializers import StreamSerializer
from beer.apps.data_source.api.serializers import EventSerializer

import logging
logger = logging.getLogger('django.request')


class StreamViewSet(viewsets.ModelViewSet):
    model = Stream
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()


class StreamEventsViewSet(viewsets.ModelViewSet):
    model = Stream
    serializer_class = EventSerializer
    queryset = Stream.objects.all()
