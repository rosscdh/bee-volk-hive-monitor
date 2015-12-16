# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

import urlparse

register = template.Library()

import logging
logger = logging.getLogger('django.request')


@register.simple_tag
def admin_url_for(instance):
    content_type = ContentType.objects.get(model=instance._meta.model.__name__.lower())
    return reverse('admin:{app_name}_{model_name}_change'.format(app_name=content_type.app_label, model_name=content_type.model), args=(instance.pk,))

