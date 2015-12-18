# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status

from pinax.eventlog.models import Log
from rest_framework.permissions import AllowAny

from beer.apps.box.models import Box
from beer.apps.sensor.models import Sensor

from ..signals.base import log_bet_event, log_influx_event
from .serializers import LogSerializer


class EventCreate(generics.ListCreateAPIView):
    """
    """
    model = Log
    serializer_class = LogSerializer
    queryset = Log.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            # try get form data
            request_data = request.data.dict().copy()
        except AttributeError:
            # is plain json data
            request_data = request.data.copy()

        sender = request_data.get('sender', None)
        sensor_action = request_data.get('sensor_action', None)

        device_id = request_data.get('tags', {}).get('device_id')
        if device_id:
            device, device_is_new = Box.objects.get_or_create(device_id=device_id)

        sensor_id = request_data.get('tags', {}).get('sensor_id')
        if sensor_id:
            sensor, sensor_is_new = Sensor.objects.get_or_create(uuid=sensor_id)
            if sensor_action:
                for action in sensor_action.split(','):
                    sensor.data[action] = request_data.get(action)
                sensor.save(update_fields=['data'])

        source = 'github' if request.META.get('X-Github-Event', None) is not None else None
        request_data['source'] = source

        if sender:
            request_data['original_sender'] = sender

        log_bet_event.send(sender=self, action='created', **request_data)

        if sensor_action is not None:
            log_influx_event.send(sender=self, action=sensor_action, **request_data)

        return Response({'message': 'created'}, status=http_status.HTTP_201_CREATED)
