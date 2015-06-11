# -*- coding: utf-8 -*-
from rest_framework import serializers


class NamedTupleValueField(serializers.Field):
    name = None
    namedtuple = None

    def __init__(self, name, namedtuple, *args, **kwargs):
        self.name = name
        self.namedtuple = namedtuple
        return super(NamedTupleValueField, self).__init__(*args, **kwargs)

    def to_representation(self, data):
        return unicode(self.namedtuple.get_choices_dict().get(data, 'Unknown'), "utf-8")

    def to_internal_value(self, data):
        return data
