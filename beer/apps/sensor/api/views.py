# -*- coding: utf-8 -*-
from rest_framework import viewsets

from rulez import registry as rulez_registry

from ..models import (Sensor,)
from .serializers import (SensorSerializer,)

# import logging
# logger = logging.getLogger('django.request')


class SensorViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(boxes__in=self.request.user.box_set.all())

    # def create(self, request):
    #     if self.request.method == 'POST':
    #         self.request.data['users'] = [self.request.user.pk]
    #         latitude = self.request.data.get('latitude', '51.1935462')
    #         longitude = self.request.data.get('longitude', '6.4479122999999845')
    #         #import pdb;pdb.set_trace()
    #         self.request.data['position'] = Geoposition(latitude, longitude)

    #     return super(SensorViewSet, self).create(request)

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
