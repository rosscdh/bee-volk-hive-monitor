# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from rulez import registry as rulez_registry

from beer.apps.project.models import Project
from beer.pusher_services import PusherAuthService

from ..models import (Box,)
from .serializers import (BoxSerializer,)

import logging
logger = logging.getLogger('django.request')


class BoxViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        return user == self.get_object().owner or user.is_staff

    def can_delete(self, user):
        return user == self.get_object().owner or user.is_staff


rulez_registry.register("can_read", BoxViewSet)
rulez_registry.register("can_edit", BoxViewSet)
rulez_registry.register("can_delete", BoxViewSet)


class BoxRegistrationEndpoint(generics.CreateAPIView):
    model = Box
    serializer_class = BoxSerializer

    def create(self, request, **kwargs):
        status_code = status.HTTP_200_OK

        request_data = request.data.copy()
        request_data['remote_ip'] = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

        extra_data = {}

        mac_address = request.data.get('mac_address')

        box, is_new = self.model.objects.get_or_create(mac_address=mac_address)

        serializer = self.serializer_class(box,
                                           request_data,
                                           context={'request': request})

        if serializer.is_valid() is True:

            serializer.save()

            response = {
                'box': serializer.data,
                'is_new': is_new,
            }
            response.update(extra_data)

        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = serializer.errors

        return Response(response, status_code)


class BoxPusherPresenceAuthEndpoint(views.APIView):
    def post(self, request, **kwargs):
        s = PusherAuthService(channel_name=request.DATA.get('channel_name'),
                              socket_id=request.DATA.get('socket_id'))
        json_data = s.process()
        return Response(json_data)
