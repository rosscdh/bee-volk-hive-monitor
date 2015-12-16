# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Hive


class HiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        exclude = ('data',)
