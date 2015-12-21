# -*- coding: utf-8 -*-
from django.db import models

from shortuuidfield import ShortUUIDField as UUIDField
from jsonfield import JSONField
from geoposition.fields import GeopositionField


class Box(models.Model):
    slug = UUIDField(auto=True,
                     db_index=True)
    owner = models.ForeignKey('auth.User', blank=True, null=True)
    name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    mac_address = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    device_id = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    position = GeopositionField(default='51.1935462,6.4479122999999845', null=True, blank=True)
    data = JSONField(default={})

    @property
    def remote_ip(self):
        return self.data.get('remote_ip', None)

    @remote_ip.setter
    def remote_ip(self, value):
        self.data['remote_ip'] = value

    def __unicode__(self):
        return '%s' % self.slug
