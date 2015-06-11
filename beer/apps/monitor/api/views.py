# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
# from rest_framework_extensions.mixins import CacheResponseMixin

from ..models import MonitorSite, UrlLog
from .serializers import MonitorSiteSerializer, UrlSerializer, CreateUrlSerializer, CompareUrlSerializer, UrlLogSerializer
from ..services import FetchUrlService


# class MonitorViewset(CacheResponseMixin,
#                      viewsets.ReadOnlyModelViewSet):
class MonitorViewset(viewsets.ModelViewSet):
    """
    Views showing more information about the posts
    """
    model = MonitorSite
    serializer_class = MonitorSiteSerializer
    queryset = MonitorSite.objects.all()


class FetchUrlView(generics.CreateAPIView):
    model = UrlLog
    serializer_class = CreateUrlSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.DATA)
        data = {'log': {'object': None}}

        if serializer.is_valid():
            s = FetchUrlService(url=serializer.validated_data['url'])
            data = s.process()

        return Response(UrlLogSerializer(data.get('log').get('object')).data)


class DiffUrlView(generics.RetrieveAPIView):
    """
    Compare 2 UrlLog object contents
    """
    model = UrlLog
    serializer_class = CompareUrlSerializer

    def get(self, request, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        data = {}

        if serializer.is_valid() is True:
            data = serializer.data

        return Response(data)
