# -*- coding: utf-8 -*-
from django.db import models

from rulez import registry as rulez_registry

from uuidfield import UUIDField
from jsonfield import JSONField
from geoposition.fields import GeopositionField


class Hive(models.Model):
    uuid = UUIDField(auto=True)
    users = models.ManyToManyField('auth.User')
    name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    project = models.ForeignKey('project.Project', null=True, blank=True)
    position = GeopositionField()
    data = JSONField(default={})

    def get_position(self):
        return {
            'latitude': getattr(self.position, 'latitude', None),
            'longitude': getattr(self.position, 'longitude', None),
        }

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        return user in self.users.all() or user.is_staff

    def can_delete(self, user):
        return user in self.users.all() or user.is_staff


rulez_registry.register("can_read", Hive)
rulez_registry.register("can_edit", Hive)
rulez_registry.register("can_delete", Hive)
