# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.fields import Field, SkipField


class JSONDataAttributeField(serializers.Field):
    def __init__(self, key=None, *args, **kwargs):
        super(JSONDataAttributeField, self).__init__(*args, **kwargs)
        self.key = self.field_name if key is None else key
        # setattr(self.parent, self._local_source_name, {})  # reset the storage

    @property
    def _local_source_name(self):
        return '_local_%s' % self.source

    @property
    def key_name(self):
        return self.field_name if self.key is None else self.key

    def to_internal_value(self, data):
        """
        return the complete JSON object; taken from the parent instance
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


class NamedModelField(Field):
    """
    A read-only field that emulates a standard SerializerMethodField by reading from a data attribute.  This is
     useful for flattened queries with 'nested' values.  For example:

     user_code = NamedModelField("client__user__code", "")  is equivilant to

     def get_user_code(self, obj):
         return obj.get("client__user__code", "")
    """

    def __init__(self, source=None, default='', **kwargs):
        self.source_field_name = source
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        kwargs.setdefault('default', default)
        super(NamedModelField, self).__init__(**kwargs)

    def to_representation(self, obj):
        try:
            if hasattr(obj, 'get') is True:
                return obj.get(self.source_field_name, self.get_default())
            else:
                raise NotImplementedError("This can only be used with data retrieved using a call to .values(), not "
                                          "with an actual model instance.  If you ware working against raw model "
                                          "instances, then try using NestedModelField('%s')" %
                                          self.source_field_name.replace("__", "."))
        except SkipField:
            pass

        return self.get_default()


class NestedModelField(Field):
    """
    A read-only field that emulates a standard SerializerMethodField by reading from a data attribute.  This is
     useful for flattened queries with 'nested' values.  For example:

     user_code = NestedModelField("client.user.code", default="")  is equivilant to

     def get_user_code(self, obj):
        if obj.client and obj.client.user:
            return obj.client.user.code

    Try to pre-fetch the data that will be used here by calling .selected_related()
    def get_queryset(self):
        return Client.objects.select_related('user').all()
    """

    def __init__(self, source=None, default='', **kwargs):
        self.source_field_name = source
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        kwargs['default'] = default
        super(NestedModelField, self).__init__(**kwargs)

    def to_representation(self, obj):
        current = obj
        for key in self.source_field_name.split('.'):
            if hasattr(current, key):
                current = getattr(current, key)
            else:
                return self.get_default()
        return current

    def to_internal_value(self, data):
        pass
