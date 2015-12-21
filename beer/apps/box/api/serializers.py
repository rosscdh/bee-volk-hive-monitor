# -*- coding: utf-8 -*-
from rest_framework import serializers

from beer.apps.sensor.api.serializers import SensorSerializer

from ..models import Box


class BoxSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    remote_ip = serializers.IPAddressField(read_only=True)
    mac_address = serializers.CharField(read_only=True)
    device_id = serializers.CharField(read_only=True)
    sensors = serializers.SerializerMethodField()

    class Meta:
        model = Box
        exclude = ('data',)

    def create(self, validated_data):
        instance, is_new = self.Meta.model.objects.get_or_create(slug=self.initial_data.get('uuid'))
        return instance

    def get_name(self, obj):
        return 'HiveEmpire-Sense device' if obj.name in [None, ''] else obj.name

    def get_sensors(self, obj):
        return SensorSerializer(obj.sensor_set.all(), many=True).data
