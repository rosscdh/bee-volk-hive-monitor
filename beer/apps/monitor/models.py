# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField


class Url(models.Model):
    url = models.URLField(max_length=255, db_index=True)
    schema = models.CharField(max_length=10, db_index=True, null=True)
    host = models.CharField(max_length=128, db_index=True, null=True)
    port = models.CharField(max_length=4, db_index=True, null=True)
    query_string = models.CharField(max_length=255, db_index=True, null=True)
    data = JSONField(default={})


class MonitorSite(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=128, db_index=True)
    task = models.ForeignKey('djcelery.PeriodicTask')
    schedule = models.ForeignKey('djcelery.IntervalSchedule')
    urls = models.ManyToManyField('monitor.Url')
    data = JSONField(default={})
