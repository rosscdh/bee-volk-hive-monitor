# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

import urllib

register = template.Library()

SOCIAL_SHARE_PROVIDERS = {
    'facebook': 'https://www.facebook.com/sharer/sharer.php?u={{ url }}',
    'twitter': 'https://twitter.com/intent/tweet?url={{ url }}',
    'googleplus': 'https://plus.google.com/share?url={{ url }}',
    'linkedin': 'https://www.linkedin.com/shareArticle?mini=true&url={{ url }}',
    'xing': 'https://www.xing.com/app/user?op=share;url={{ url }}'
}


@register.inclusion_tag('partials/social_share.html')
def social_share(url):
    social_share = {}

    for key, share_url in SOCIAL_SHARE_PROVIDERS.iteritems():
        t = template.Template(share_url)
        social_share[key] = t.render(template.Context({'url': urllib.quote_plus(url)}))

    return {
        'STATIC_URL': settings.STATIC_URL,
        'SOCIAL_SHARE_LINKS': social_share
    }
