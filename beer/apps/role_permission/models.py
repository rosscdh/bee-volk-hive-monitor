# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

from .roles import ROLES
from .mixins import PermissionProviderMixin


User.add_to_class('ROLES', ROLES)


class Participant(PermissionProviderMixin,
                  models.Model):
    """
    Model to store the Users permissions with regards to a project
    """
    stream = models.ForeignKey('stream.Stream')
    user = models.ForeignKey('auth.User')
    is_owner = models.BooleanField(default=False,
                                   db_index=True)  # is this user a matter owner
    role = models.IntegerField(choices=ROLES.get_choices(),
                               default=ROLES.noone,
                               db_index=True)  # default to client to meet the original requirements
    data = JSONField(default={})

    def __unicode__(self):
        return '%s (%s)' % (self.user, self.display_role)

    @property
    def display_role(self):
        return self.ROLES.get_desc_by_value(self.role)

    @property
    def role_name(self):
        return self.ROLES.get_name_by_value(self.role)

    def default_permissions(self, user_class=None):
        """
        @TODO ross update according to beer roles
        Class to provide a wrapper for user permissions
        The default permissions here MUST be kept up-to-date with the Product.Meta.permissions tuple
        user_class (string) allow for override of user class defaults, upgrading a user
        """
        if self.role in [self.ROLES.brand_account_admin, self.ROLES.printer_account_admin] or user_class in ['brand_account_admin', 'printer_account_admin']:
            return self.OWNER_PERMISSIONS

        # cater to various roles
        if self.role in [self.ROLES.brand_manager] or user_class in ['brand_manager']:
            # Lawyers currently can do everything the owner can except clients and participants
            return self.PRIVILEGED_USER_PERMISSIONS

        elif self.role in [self.ROLES.printer_operator] or user_class in ['printer_operator']:
            # Clients by default can currently see all items (allow by default)
            return self.UNPRIVILEGED_USER_PERMISSIONS

        # Anon permissions, for anyone else that does not match
        return self.ANONYMOUS_USER_PERMISSIONS

    @classmethod
    def clean_permissions(cls, **kwargs):
        """
        Pass in a set of permissions and remove those that do not exist in
        the base set of permissions
        """
        kwargs_to_test = kwargs.copy()  # clone the kwargs dict so we can pop on it

        for permission in kwargs:
            if permission not in cls.PERMISSIONS:
                kwargs_to_test.pop(permission)
                # @TODO ? need to check for boolean value?
        return kwargs_to_test

    @property
    def permissions(self):
        """
        combine the default permissions and override with the specific users
        permissions; this allows for the addition of new permissions easily
        """
        permissions_to_return = self.default_permissions().copy()  # copy the dict to stop changes happening
        user_permissions = self.data.get('permissions', permissions_to_return)  # get users current permissions, defaulting to default if none exist
        permissions_to_return.update(user_permissions)  # update defaults with users current
        return permissions_to_return

    @permissions.setter
    def permissions(self, value):
        if type(value) not in [dict] and len(value.keys()) > 0:
            raise Exception('WorkspaceParticipants.permissions must be a dict of permissions %s' %
                            self.default_permissions())
        self.data['permissions'] = self.clean_permissions(**value)

    def reset_permissions(self):
        self.permissions = self.default_permissions()

    def update_permissions(self, **kwargs):
        self.permissions = kwargs

    def has_permission(self, **kwargs):
        """
        .has_permission(manage_items=True)
        """
        permissions = self.permissions
        return all(req_perm in permissions and permissions[req_perm] == value for req_perm, value in kwargs.iteritems())
