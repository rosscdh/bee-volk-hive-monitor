# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        exclude = ('data', 'boxes')
