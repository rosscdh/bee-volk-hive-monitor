# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Hive

import random


class HiveSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    sensors = serializers.SerializerMethodField()

    class Meta:
        model = Hive
        exclude = ('data', 'position')

    def get_photo(self, obj):
        return obj.data.get('photo', {'url': 'http://www.annkissam.com/sites/default/files/community-beehive-2.png', 'alt': 'Default Hive Image'})

    def get_location(self, obj):
        return {'lat': obj.position.latitude, 'lon': obj.position.longitude, 'address': obj.data.get('address')}

    def get_status(self, obj):
        return obj.data.get('status', 'no-record')

    def get_sensors(self, obj):
        return []
