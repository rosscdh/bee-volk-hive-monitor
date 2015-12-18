# -*- coding: utf-8 -*-
from rest_framework import viewsets

from rulez import registry as rulez_registry

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

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        return user in self.get_object().users.all() or user.is_staff

    def can_delete(self, user):
        return user in self.get_object().users.all() or user.is_staff


rulez_registry.register("can_read", HiveViewSet)
rulez_registry.register("can_edit", HiveViewSet)
rulez_registry.register("can_delete", HiveViewSet)
