# -*- coding: utf-8 -*-
from rest_framework import serializers

from pinax.eventlog.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        exclude = ('extra',)
