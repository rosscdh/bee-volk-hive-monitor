# -*- coding: utf-8 -*-
import django.dispatch
from django.dispatch import receiver

from .models import MonitorSite


url_log_created = django.dispatch.Signal(providing_args=['sender',
                                                         'user',
                                                         'url',
                                                         'url_log'])


@receiver(url_log_created)
def ensure_site_exists(sender, user, url, url_log, **kwargs):
    # Get the site monitor record for this url and user
    try:
        site = MonitorSite.objects.get(user=user,
                                       netloc=url.netloc)
    except MonitorSite.DoesNotExist:
        # if not present create it
        site = MonitorSite.objects.create(user=user,
                                          name=url.netloc,
                                          netloc=url.netloc)
    # add the url
    site.urls.add(url)

