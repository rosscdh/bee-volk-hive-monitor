# -*- coding: utf-8 -*-
from rest_framework import viewsets

from rulez import registry as rulez_registry
from geoposition import Geoposition

from ..models import (Hive,)
from .serializers import (HiveSerializer,)

# import logging
# logger = logging.getLogger('django.request')


class HiveViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(users__in=[self.request.user])

    def create(self, request):
        if self.request.method == 'POST':
            self.request.data['users'] = [self.request.user.pk]
            latitude = self.request.data.get('latitude', '51.1935462')
            longitude = self.request.data.get('longitude', '6.4479122999999845')
            #import pdb;pdb.set_trace()
            self.request.data['position'] = Geoposition(latitude, longitude)

        return super(HiveViewSet, self).create(request)

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        if self.request.method == 'POST':
            return True
        return user in self.get_object().users.all() or user.is_staff

    def can_delete(self, user):
        return user in self.get_object().users.all() or user.is_staff


rulez_registry.register("can_read", HiveViewSet)
rulez_registry.register("can_edit", HiveViewSet)
rulez_registry.register("can_delete", HiveViewSet)
