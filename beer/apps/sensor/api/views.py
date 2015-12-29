# -*- coding: utf-8 -*-
from rest_framework import viewsets

from rulez import registry as rulez_registry

from rest_framework.decorators import detail_route
from rest_framework.response import Response

from beer.apps.evt.signals.handlers import influx_client

from ..models import (Sensor,)
from .serializers import (SensorSerializer,)

# import logging
# logger = logging.getLogger('django.request')

class InfluxTransform(object):
    def __init__(self, data):
        self.data = data
        self.series = self.data.get('series', [])[0]

    def transform(self):
        columns = self.series.get('columns')
        for row in self.series.get('values', []):
            yield dict(zip(columns, row))

    def process(self):
        return {
            'name': self.series.get('name'),
            'data': list(self.transform())
        }


class SensorViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        if self.request.user.is_authenticated() is True:
            return self.queryset.filter(boxes__in=self.request.user.box_set.all())
        else:
            return self.queryset.all()

    # def create(self, request):
    #     if self.request.method == 'POST':
    #         self.request.data['users'] = [self.request.user.pk]
    #         latitude = self.request.data.get('latitude', '51.1935462')
    #         longitude = self.request.data.get('longitude', '6.4479122999999845')
    #         #import pdb;pdb.set_trace()
    #         self.request.data['position'] = Geoposition(latitude, longitude)

    #     return super(SensorViewSet, self).create(request)

    @detail_route()
    def chart(self, request, uuid=None):
        """
        Return the tieline of graph data to the api
        """
        #import pdb;pdb.set_trace()
        sensor = self.get_object()

        box = sensor.boxes.all().first()
        device_id = box.device_id
        resp = {'series': []}
        #device_id = '0000000055483a88'
        #device_id = '00000000d390eefe'
        #print "select value FROM humidity where device_id = '{device_id}';".format(device_id=device_id)

        for sensor_type in ['temperature', 'humidity']:
            query = "select value FROM {sensor_type} where device_id = '{device_id}' and time > now() - {time_limit};".format(device_id=device_id,
                                                                                                                              sensor_type=sensor_type,
                                                                                                                              time_limit=request.GET.get('time_limit', '1h'))
            result = influx_client.query(query)
            try:
                resp.get('series').append(result.raw.get('series')[0])
            except:
                # @TODO add log here
                pass

        return Response(resp)

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        if self.request.method == 'POST':
            return True
        return user in self.get_object().users.all() or user.is_staff

    def can_delete(self, user):
        return user in self.get_object().users.all() or user.is_staff


rulez_registry.register("can_read", SensorViewSet)
rulez_registry.register("can_edit", SensorViewSet)
rulez_registry.register("can_delete", SensorViewSet)
