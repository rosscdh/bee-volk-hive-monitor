# -*- coding: utf-8 -*-
from rest_framework import serializers
from decimal import Decimal

class GeopositionSerializerField(serializers.Field):
    DEFAULT_GEO_COORDS = ('51.1935462', '6.4479122999999845')

    def to_representation(self, obj):
        return {
            'latitude': Decimal(getattr(obj, 'latitude', self.DEFAULT_GEO_COORDS[0])),
            'longitude': Decimal(getattr(obj, 'longitude', self.DEFAULT_GEO_COORDS[1])),
        }

    def to_internal_value(self, data):
        return '%s,%s' % (Decimal(getattr(data, 'latitude', self.DEFAULT_GEO_COORDS[0])),
                          Decimal(getattr(data, 'longitude', self.DEFAULT_GEO_COORDS[1])))
