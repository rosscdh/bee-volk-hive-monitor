# -*- coding: utf-8 -*-
from rest_framework import serializers

from social.apps.django_app.default.models import UserSocialAuth
from ..models import DataSource


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource


class UserSocialAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth


class EventSerializer(serializers.Serializer):
    """
    Primary serializer for data that gets stored in the stream object
    used to convert various data_sources into something that is composable
    and displayable in the timeline
    """
    timestamp = serializers.DateTimeField()
    title = serializers.CharField(max_length=128)
    excerpt = serializers.CharField(max_length=255)
    #severity = serializers.CharField(max_length=128)
    action_type = serializers.SlugField(max_length=64, min_length=3, allow_blank=False)
    data_source = DataSourceSerializer()
    data = serializers.DictField(default={})
