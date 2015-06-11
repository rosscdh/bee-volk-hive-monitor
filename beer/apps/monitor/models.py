# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField


class Url(models.Model):
    url = models.URLField(max_length=255, db_index=True)

    scheme = models.CharField(max_length=10, db_index=True, null=True)
    netloc = models.CharField(max_length=128, db_index=True, null=True)
    path = models.CharField(max_length=128, db_index=True, null=True)
    params = models.CharField(max_length=128, db_index=True, null=True)
    query = models.CharField(max_length=128, db_index=True, null=True)
    fragment = models.CharField(max_length=128, db_index=True, null=True)

    data = JSONField(default={})


class UrlLog(models.Model):
    url = models.ForeignKey('monitor.Url')
    digest = models.CharField(max_length=255, db_index=True)
    date_of = models.DateTimeField(auto_now=False, auto_now_add=True)
    data = JSONField(default={})


class MonitorSite(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=128, db_index=True)
    task = models.ForeignKey('djcelery.PeriodicTask')
    schedule = models.ForeignKey('djcelery.IntervalSchedule')
    urls = models.ManyToManyField('monitor.Url')
    data = JSONField(default={})
