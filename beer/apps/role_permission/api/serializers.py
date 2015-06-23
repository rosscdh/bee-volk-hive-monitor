# -*- coding: utf-8 -*-
from django.template.defaultfilters import filesizeformat
from rest_framework import serializers


class RoleSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        return obj.get('permissions', [])
