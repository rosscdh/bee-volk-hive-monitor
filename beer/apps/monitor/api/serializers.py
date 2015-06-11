# -*- coding: utf-8 -*-
from rest_framework import serializers

from djcelery.models import (PeriodicTask, IntervalSchedule)
from djcelery.models import PERIOD_CHOICES

from ..models import Url, UrlLog, MonitorSite

import difflib
DIFFER = difflib.Differ()


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
        exclude = ('data',)


class CreateUrlSerializer(serializers.Serializer):
    url = serializers.URLField(allow_null=True)


class CompareUrlSerializer(serializers.Serializer):
    a_pk = serializers.PrimaryKeyRelatedField(queryset=UrlLog.objects.all(), allow_null=False)
    b_pk = serializers.PrimaryKeyRelatedField(queryset=UrlLog.objects.all(), allow_null=False)
    diff = serializers.SerializerMethodField()

    def get_diff(self, obj):
        a = obj.get('a_pk').data.get('content')
        b = obj.get('b_pk').data.get('content')

        diff = difflib.unified_diff(a, b, lineterm='')
        return '\n'.join(list(diff))


class UrlLogSerializer(serializers.ModelSerializer):
    url = UrlSerializer()

    content =  serializers.CharField(source='data.content')

    previous = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    class Meta:
        model = UrlLog
        exclude = ('data',)

    def get_previous(self, obj):
        previous = obj.__class__.objects.exclude(pk=obj.pk).filter(url=obj.url, pk__lt=obj.pk).first()
        if previous is not None:
            return previous.pk
        return None

    def get_next(self, obj):
        next = obj.__class__.objects.exclude(pk=obj.pk).filter(url=obj.url, pk__gt=obj.pk).first()
        if next is not None:
            return next.pk
        return None


class MonitorSiteSerializer(serializers.ModelSerializer):
    schedule = IntervalScheduleSerializer()
    #task = PeriodicTaskSerializer()  # caculated automatically based on wether or not the schedule has changed
    urls = UrlSerializer(many=True)

    class Meta:
        model = MonitorSite
        exclude = ('data', 'task',)
