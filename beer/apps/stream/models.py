# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals

from jsonfield import JSONField

from beer.utils.signals import ensure_model_slug

import logging
logger = logging.getLogger('django.request')


class Stream(models.Model):
    """
    Base User Profile, where we store all the interesting information about
    users
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)

    auth_provider = models.ForeignKey('default.UserSocialAuth', blank=True, null=True)  # need to make a PR with pyhton-social-auth to fix their app name

    data_sources = models.ManyToManyField('data_source.DataSource')

    data = JSONField(default={})

    def __unicode__(self):
        return '%s <%s>' % (self.name, self.slug)


#
# Signals
#
signals.pre_save.connect(ensure_model_slug,
                         sender=Stream,
                         dispatch_uid='stream.pre_save.ensure_model_slug')
