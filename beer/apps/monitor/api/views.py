# -*- coding: utf-8 -*-
from rest_framework import viewsets
# from rest_framework_extensions.mixins import CacheResponseMixin

from ..models import MonitorSite
from .serializers import MonitorSiteSerializer


# class MonitorViewset(CacheResponseMixin,
#                      viewsets.ReadOnlyModelViewSet):
class MonitorViewset(viewsets.ModelViewSet):
    """
    Views showing more information about the posts
    """
    model = MonitorSite
    serializer_class = MonitorSiteSerializer
    queryset = MonitorSite.objects.all()
