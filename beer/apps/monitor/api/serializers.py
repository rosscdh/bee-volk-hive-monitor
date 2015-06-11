# -*- coding: utf-8 -*-
from rest_framework import serializers

from djcelery.models import (PeriodicTask, IntervalSchedule)
from djcelery.models import PERIOD_CHOICES

from ..models import Url, MonitorSite


class IntervalScheduleSerializer(serializers.Serializer):
    every = serializers.ChoiceField(choices=PERIOD_CHOICES)
    period = serializers.IntegerField()

    class Meta:
        model = IntervalSchedule


class PeriodicTaskSerializer(serializers.Serializer):
    class Meta:
        model = PeriodicTask
        exclude = ('data',)


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url


class MonitorSiteSerializer(serializers.ModelSerializer):
    schedule = IntervalScheduleSerializer()
    #task = PeriodicTaskSerializer()  # caculated automatically based on wether or not the schedule has changed
    urls = UrlSerializer(many=True)

    class Meta:
        model = MonitorSite
        exclude = ('data', 'task',)
