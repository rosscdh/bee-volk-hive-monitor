# -*- coding: utf-8 -*-
from rest_framework import serializers

from beer.apps.data_source.api.serializers import DataSourceSerializer

from ..models import Stream


class StreamSerializer(serializers.ModelSerializer):
    data_sources = DataSourceSerializer(many=True)

    class Meta:
        model = Stream
        exclude = ('data',)
