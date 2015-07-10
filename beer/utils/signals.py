# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify

from beer.utils.app import _model_slug_exists

import uuid
import logging
logger = logging.getLogger('django.request')


def ensure_model_slug(sender, instance, **kwargs):
    """
    signal to handle creating a instance.__class__ slug
    """
    slug = getattr(instance, 'slug', False)
    name = getattr(instance, 'name', False)

    if slug is False or name is False:
        raise Exception('Object "%s (%s)" must have slug and name fields' % (instance, instance.__class__))

    # if we have no slug
    # or we have an object
    if instance.slug in [None, ''] or instance.pk and instance.slug and instance.__class__.objects.exclude(pk=instance.pk).filter(slug=instance.slug):
        final_slug = slugify(instance.name)[:32]  # initial slug, limited to 32 in length
        #
        # @DANGER @TODO change to a limited xrange? instead of a while?
        #
        while _model_slug_exists(model=instance.__class__.objects.model,
                                 slug=final_slug):
            logger.info('%s %s exists, trying to create another' % (instance.__class__, final_slug))

            slug = '%s-%s' % (final_slug, uuid.uuid4().get_hex()[:4]) #append the hex
            slug = slug[:30]  # substr it to 30 in length
            final_slug = slugify(slug)  # reslugify that slug to be a slug

        instance.slug = final_slug
