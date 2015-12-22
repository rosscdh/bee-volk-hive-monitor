# -*- coding: utf-8 -*-
from rest_framework import serializers

from pinax.eventlog.models import Log

from beer.apps.api.fields import GeopositionSerializerField
from beer.apps.sensor.api.serializers import SensorSerializer

from ..models import Hive


class HiveSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    sensors = SensorSerializer(many=True)
    position = GeopositionSerializerField()
    event_log = serializers.SerializerMethodField()

    class Meta:
        model = Hive
        exclude = ('data',)

    def get_photo(self, obj):
        return obj.data.get('photo', {'url': 'http://www.annkissam.com/sites/default/files/community-beehive-2.png', 'alt': 'Default Hive Image'})

    def get_address(self, obj):
        return obj.data.get('address')

    def get_status(self, obj):
        return obj.data.get('status', 'no-record')

    def get_event_log(self, obj):
        #return Log.objects.filter()
        return []

