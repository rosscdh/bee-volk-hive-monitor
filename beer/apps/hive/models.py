# -*- coding: utf-8 -*-
from django.db import models

from uuidfield import UUIDField
from jsonfield import JSONField
from geoposition.fields import GeopositionField


class Hive(models.Model):
    uuid = UUIDField(auto=True,
                     db_index=True,
                     null=True)
    name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField('auth.User')
    project = models.ForeignKey('project.Project', null=True, blank=True)
    position = GeopositionField()
    data = JSONField(default={})
