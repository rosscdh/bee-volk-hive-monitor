# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import (Hive,)
from .serializers import (HiveSerializer,)

# import logging
# logger = logging.getLogger('django.request')


class HiveViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    lookup_field = 'slug'
