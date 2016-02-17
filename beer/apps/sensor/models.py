# -*- coding: utf-8 -*-
from django.db import models

from rulez import registry as rulez_registry

from shortuuidfield import ShortUUIDField as UUIDField
from jsonfield import JSONField

from beer.utils import get_namedtuple_choices

SENSOR_TYPES = get_namedtuple_choices('SENSOR_TYPES', (
    ('temperature_humidity', 'temperature_humidity', 'Temperature & Humidity'),
    ('weight', 'weight', 'Hive Weight'),
    ('in_out_counter', 'in_out_counter', 'In/Out Counter'),
    ('video_stream', 'video_stream', 'Video Stream'),
))

SENSOR_STATUSES = get_namedtuple_choices('SENSOR_STATUSES', (
    ('unknown', 'unknown', 'Unknown'),
    ('receiving', 'receiving', 'Receiving'),
    ('disconnected', 'disconnected', 'Disconnected'),
))

API_VERSIONS = get_namedtuple_choices('SENSOR_STATUSES', (
    (1, 'v1', 'Version 1 (Wired)'),
    (2, 'v2', 'Version 2 (Wireless)'),
))


class Sensor(models.Model):
    SENSOR_TYPES = SENSOR_TYPES
    SENSOR_STATUSES = SENSOR_STATUSES

    uuid = UUIDField(auto=True, db_index=True)
    name = models.CharField(choices=SENSOR_TYPES.get_choices(), max_length=128, db_index=True)
    status = models.CharField(choices=SENSOR_STATUSES.get_choices(), max_length=128, db_index=True)
    boxes = models.ManyToManyField('box.Box')
    version = models.IntegerField(choices=API_VERSIONS.get_choices(), db_index=True)
    data = JSONField(default={})

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.uuid)

    def can_read(self, user):
        return user.is_authenticated()

    def can_edit(self, user):
        return True

    def can_delete(self, user):
        return True


rulez_registry.register("can_read", Sensor)
rulez_registry.register("can_edit", Sensor)
rulez_registry.register("can_delete", Sensor)
