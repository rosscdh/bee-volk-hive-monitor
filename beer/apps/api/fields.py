# -*- coding: utf-8 -*-
from rest_framework import serializers


class GeopositionSerializerField(serializers.Field):
    DEFAULT_GEO_COORDS = ('51.1935462', '6.4479122999999845')

    def to_representation(self, obj):
        return {
            'latitude': str(getattr(obj, 'latitude', self.DEFAULT_GEO_COORDS[0])),
            'longitude': str(getattr(obj, 'longitude', self.DEFAULT_GEO_COORDS[1])),
        }

    def to_internal_value(self, data):
        return '%s,%s' % (str(getattr(data, 'latitude', self.DEFAULT_GEO_COORDS[0])),
                          str(getattr(data, 'longitude', self.DEFAULT_GEO_COORDS[1])))
