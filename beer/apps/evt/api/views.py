# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify

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

    ACTION_MATRIX = {
        'temp': 'temperature',
        't': 'temperature',
        'h': 'temperature',
    }

    def transpose_action(self, action):
        # return the converted action or no match so return the original action
        action = slugify(action)  # slugify the name
        return self.ACTION_MATRIX.get(action, action)

    def create(self, request, *args, **kwargs):

        try:
            # try get form data
            request_data = request.data.dict().copy()

        except AttributeError:
            # is plain json data
            request_data = request.data.copy()

        api_version = request_data.get('api_version', 1)  # Default to 1
        sensor_action = request_data.get('sensor_action', '')

        device_id = request_data.get('tags', {}).get('device_id')
        sensor_id = request_data.get('tags', {}).get('sensor_id')

        if device_id:

            device, device_is_new = Box.objects.get_or_create(device_id=device_id)

            if api_version in [1]:
                #
                # @TODO this is temp while we only have v1 sensors
                # set the devices temp sensors to have the provided data
                # Remove once we start sending the specific sensor id
                #
                device.sensor_set.filter(version=api_version).update(data=request_data)

        if sensor_id:

            sensor, sensor_is_new = Sensor.objects.get_or_create(uuid=sensor_id,
                                                                 version=api_version)

            if sensor_action:
                # Extract the sensor_actions from the sensor data
                for action in sensor_action.split(','):
                    sensor.data[self.transpose_action(action=action)] = request_data.get(action)

                sensor.save(update_fields=['data'])
                log_influx_event.send(sender=self,
                                      action=sensor_action,
                                      **request_data)

        log_bet_event.send(sender=self,
                           action='created',
                           **request_data)


        return Response({'message': 'created'}, status=http_status.HTTP_201_CREATED)
