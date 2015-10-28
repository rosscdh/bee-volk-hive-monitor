# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Box


class BoxSerializer(serializers.ModelSerializer):
    remote_ip = serializers.IPAddressField()

    class Meta:
        model = Box
        exclude = ('data',)
