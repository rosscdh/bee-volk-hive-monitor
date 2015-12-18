# -*- coding: utf-8 -*-
from rest_framework import serializers

from beer.apps.api.fields import NamedTupleValueField

from ..models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    name = NamedTupleValueField(Sensor.SENSOR_TYPES, display_attribute='description', read_only=True)
    status = NamedTupleValueField(Sensor.SENSOR_STATUSES, display_attribute='description', read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        exclude = ('boxes',)

    def get_value(self, obj):
        if obj.name == Sensor.SENSOR_TYPES.temperature_humidity:
            return u'%s℃/%s' % (obj.data.get('temperature'), obj.data.get('humidity'))
