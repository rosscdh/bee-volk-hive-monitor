# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import viewsets

from .serializers import (UserSerializer,)


class MeView(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self, *args, **kwargs):
        # filter the scans based on the current project -
        return self.model.objects.get(pk=self.request.user.pk)


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def __init__(self, **kwargs):
        super(UserViewSet, self).__init__(**kwargs)

    def get_queryset(self):
        query = User.objects.filter(client=self.request.user.client)
        # filter out is_staff users (for now?) to avoid them showing up in the list of "users" that a
        # client sees.  this will happen when the STE is in the company, validating equipment and such
        query = query.filter(is_staff=False)
        #
        return query
