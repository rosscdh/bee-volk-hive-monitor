# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Stream


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
