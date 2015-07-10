# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from ..models import Stream
from .serializers import StreamSerializer

import logging
logger = logging.getLogger('django.request')


class StreamViewSet(viewsets.ModelViewSet):
    model = Stream
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()

    @list_route(methods=['GET'])
    def stream_data(self, *args, **kwargs):
        return Response([])
