# -*- coding: utf-8 -*-
from django.db import models

from uuidfield import UUIDField
from jsonfield import JSONField


class Box(models.Model):
    slug = UUIDField(auto=True,
                     db_index=True,
                     null=True)
    name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    mac_address = models.CharField(max_length=64, db_index=True)
    device_id = models.CharField(max_length=64, db_index=True)
    # project = models.ForeignKey('project.Project', null=True, blank=True)
    # playlist = models.ForeignKey('playlist.Playlist', null=True, blank=True)
    data = JSONField(default={})

    @property
    def remote_ip(self):
        return self.data.get('remote_ip', None)

    @remote_ip.setter
    def remote_ip(self, value):
        self.data['remote_ip'] = value

    def __unicode__(self):
        return '%s - %s (%s)' % (self.name, self.device_id, self.remote_ip)
