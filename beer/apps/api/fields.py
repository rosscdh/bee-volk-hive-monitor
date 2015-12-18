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


class NamedTupleValueField(serializers.Field):
    display_attribute = 'slug'
    namedtuple = None

    def __init__(self, namedtuple, display_attribute='slug', *args, **kwargs):
        self.display_attribute = display_attribute
        self.namedtuple = namedtuple
        return super(NamedTupleValueField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        # passed an int in
        if type(data) in [int, float]:
            return data

        if type(data) in [str, unicode]:
            # try by slug/name
            value = self.namedtuple.get_value_by_name(data)
            if value is not False:
                return value
            # try by description
            value = self.namedtuple.get_value_by_desc(data)
            if value is not False:
                return value
        return data

    def to_representation(self, data):
        if self.display_attribute in ['slug', 'name']:
            return self.namedtuple.get_name_by_value(data)
        elif self.display_attribute in ['desc', 'description']:
            return self.namedtuple.get_desc_by_value(data)
        elif self.display_attribute in ['value']:
            return data

        return self.namedtuple.get_choices_dict().get(data, 'Unknown')


class JSONDataAttributeField(serializers.Field):
    def __init__(self, key=None, *args, **kwargs):
        super(JSONDataAttributeField, self).__init__(*args, **kwargs)
        self.key = self.field_name if key is None else key

    @property
    def _local_source_name(self):
        return '_local_%s' % self.source

    @property
    def key_name(self):
        return self.field_name if self.key is None else self.key

    def get_value(self, dictionary):
        # If the user *did not pass the field* at all in the incoming JSON (not a bad-value issue)
        if self.key_name not in dictionary:
            # @todo: should this respect 'required'? be part of run_validation?
            return self.get_default()
        return super(JSONDataAttributeField, self).get_value(dictionary)

    def to_internal_value(self, data):
        """
        Return the complete JSON object; taken from the parent instance
        but remember to update the value of the specified key
        have to save the local json into a parent objects faked
        """
        json_field_data = getattr(self.parent.instance, self.source, getattr(self.parent, self._local_source_name, {}))
        json_field_data[self.key_name] = data
        # save this locally so we can access it
        setattr(self.parent, self._local_source_name, json_field_data)
        return getattr(self.parent, self._local_source_name)

    def to_representation(self, data):
        return data.get(self.key_name, self.get_default())
