# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.decorators import detail_route

from ..signals.base import log_bet_event, log_influx_event

from pinax.eventlog.models import Log
from .serializers import LogSerializer


class EventCreate(generics.ListCreateAPIView):
    """
    """
    model = Log
    serializer_class = LogSerializer
    queryset = Log.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # try get form data
            request_data = request.data.dict().copy()
        except AttributeError:
            # is plain json data
            request_data = request.data.copy()

        sender = request_data.get('sender', None)
        sensor_action = request_data.get('sensor_action', None)

        source = 'github' if request.META.get('X-Github-Event', None) is not None else None

        request_data['source'] = source

        if sender:
            request_data['original_sender'] = sender

        log_bet_event.send(sender=self, action='created', **request_data)

        if sensor_action is not None:
            log_influx_event.send(sender=self, action=sensor_action, **request_data)

        return Response({'message': 'created'}, status=http_status.HTTP_201_CREATED)
