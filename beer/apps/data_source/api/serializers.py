# -*- coding: utf-8 -*-
from rest_framework import serializers

from social.apps.django_app.default.models import UserSocialAuth

from ..models import DataSource


class UserSocialAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
