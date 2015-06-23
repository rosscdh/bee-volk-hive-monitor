# -*- coding: utf-8 -*-
from rest_framework import views
from rest_framework.response import Response

from ..models import Participant
from ..roles import ROLES
from ..mixins import PermissionProviderMixin
from .serializers import RoleSerializer

import logging
logger = logging.getLogger('django.request')


class RoleView(views.APIView):
    model = Participant  # not really this is just to user the generics view
    serializer_class = RoleSerializer
    queryset = Participant.objects.all()  # not really this is just to user the generics view

    def get(self, request, *args, **kwargs):
        roles_list = [{'id': id, 'slug': slug, 'name': name, 'permissions': PermissionProviderMixin.permissions_by_role(role=slug)} for id, slug, name in ROLES.get_all()]
        return Response(roles_list)
