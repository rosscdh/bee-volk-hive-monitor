# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError

from rest_hooks.signals import raw_hook_event

from pinax.eventlog.models import Log
from rest_framework.permissions import AllowAny

from beer.apps.box.models import Box
from beer.apps.sensor.models import Sensor

from ..signals.base import log_bet_event, log_influx_event
from .serializers import LogSerializer

import logging
logger = logging.getLogger('django.request')


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

    def send_webhooks(self, user, data):
        if not user:
            logger.error('Could not send webhook, No user specified')
        else:
            logger.error('Sending webhook')

            raw_hook_event.send(
                sender=self.__class__,
                event_name='event.webhook.send',
                payload=data,
                user=user
            )

    def create(self, request, *args, **kwargs):

        try:
            # try get form data
            request_data = request.data.dict().copy()

        except AttributeError:
            # is plain json data
            if hasattr(request.data, '__iter__') is True:
                # is a list
                request_data = request.data
            else:
                # Copy it and make it a list
                request_data = [request.data.copy()]

        #
        # Loop over the posted data
        #
        for item in request_data:

            api_version = item.get('api_version', 1)  # Default to 1
            sensor_action = item.get('sensor_action', '')

            device_id = item.get('tags', {}).get('device_id')
            sensor_id = item.get('tags', {}).get('sensor_id')

            #
            # Perform device (HiveEmpire-Sense) operations
            #
            if not device_id:
                raise ValidationError('You must provide a HiveEmpire-Sense device_id')
            else:

                device, device_is_new = Box.objects.get_or_create(device_id=device_id)

                if api_version in [1]:
                    #
                    # @TODO this is temp while we only have v1 sensors
                    # set the devices temp sensors to have the provided data
                    # Remove once we start sending the specific sensor id
                    #
                    device.sensor_set.filter(version=api_version).update(data=item)

            #
            # Perform specific sensor operations
            #
            if not sensor_id:
                raise ValidationError('You must provide a HiveEmpire sensor_id')
            else:
                sensor, sensor_is_new = Sensor.objects.get_or_create(uuid=sensor_id,
                                                                     version=api_version)

                if sensor_action:
                    # Extract the sensor_actions from the sensor data
                    for action in sensor_action.split(','):
                        #
                        # Transpose sensor names
                        #
                        sensor.data[self.transpose_action(action=action)] = item.pop(action, None)

                    sensor.save(update_fields=['data'])

                    #
                    # Send data to influx db
                    #
                    log_influx_event.send(sender=self,
                                          action=sensor_action,
                                          **item)
            #
            # Record this data as an event
            #
            log_bet_event.send(sender=self,
                               action='created',
                               **item)

        #
        # Send the Webhooks, if any
        #
        self.send_webhooks(user=device.owner,
                           data=request_data)

        return Response({'message': 'created'},
                        status=http_status.HTTP_201_CREATED)
