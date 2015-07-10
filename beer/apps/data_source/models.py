# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals

from jsonfield import JSONField

from beer.utils.signals import ensure_model_slug

import logging
logger = logging.getLogger('django.request')


class DataSource(models.Model):
    """
    Base User Profile, where we store all the interesting information about
    users
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    auth_provider = models.ForeignKey('default.UserSocialAuth')  # user is associated through this

    data = JSONField(default={})

    def __unicode__(self):
        return '%s <%s>' % (self.name, self.slug)


#
# Signals
#
signals.pre_save.connect(ensure_model_slug,
                         sender=DataSource,
                         dispatch_uid='data_stream.pre_save.ensure_model_slug')
