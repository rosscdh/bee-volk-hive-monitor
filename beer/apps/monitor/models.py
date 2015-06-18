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

    def __unicode__(self):
        return self.url

    @property
    def history(self):
        return self.urllog_set.all()


class UrlLog(models.Model):
    url = models.ForeignKey('monitor.Url')
    digest = models.CharField(max_length=255, db_index=True)
    date_of = models.DateTimeField(auto_now=False, auto_now_add=True)
    data = JSONField(default={})

    def __unicode__(self):
        return '%s (%s) on %s' % (self.url, self.digest, self.date_of)

    @property
    def screenshot(self):
        return self.data.get('capture', None)


class MonitorSite(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=128, db_index=True)
    task = models.ForeignKey('djcelery.PeriodicTask')
    schedule = models.ForeignKey('djcelery.IntervalSchedule')
    urls = models.ManyToManyField('monitor.Url')
    data = JSONField(default={})
