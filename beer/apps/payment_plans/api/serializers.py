# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from beer.apps.payment_plans.api.validators import FieldsAreEqualValidator
from beer.fields import JSONDataAttributeField


class UserSerializer(serializers.ModelSerializer):

    #role = NamedTupleValueField(source='profile__data__', namedtuple=User.ROLES, display_attribute='slug', default=User.ROLES.brand_account_admin)
    permissions = serializers.SerializerMethodField()
    language = serializers.CharField(required=False, default="en")

    title = JSONDataAttributeField(source='data', default="")
    phone = JSONDataAttributeField(source='data', default="")
    salutation = JSONDataAttributeField(source='data', default="")

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'username',)
        read_only_fields = ('last_login', 'date_joined', 'is_staff', 'is_superuser')

    def get_permissions(self, obj):
        return obj.data.get('permissions')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='Valid email address')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, max_length=100)
    new_password = serializers.CharField(required=True, write_only=True, max_length=100)
    confirm_new_password = serializers.CharField(required=True, write_only=True, max_length=100, )

    def validate_old_password(self, value):
        if not check_password(value, self.context['request'].user.password):
            raise ValidationError(_("Current password is incorrect."))
        return value

    class Meta:
        validators = [
            FieldsAreEqualValidator('new_password', 'confirm_new_password', "Passwords do not match.")
        ]
