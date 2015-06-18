# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView
from django.core.files.temp import NamedTemporaryFile

from easy_thumbnails.files import Thumbnailer, get_thumbnailer

from .models import UrlLog, Url

import base64
import os


class UrlLogScreenshotView(DetailView):
    model = UrlLog
    template_name = 'monitor/screenshot_detail.html'


class UrlLogScreenshotCompareView(DetailView):
    model = UrlLog
    template_name = 'monitor/screenshot_compare.html'

    def get_object(self, **kwargs):
        self.object = super(UrlLogScreenshotCompareView, self).get_object(**kwargs)
        self.object_b = self.model.objects.get(pk=self.kwargs.get('pk_b'))
        return self.object

    def get_context_data(self, **kwargs):
        data = super(UrlLogScreenshotCompareView, self).get_context_data(**kwargs)
        data.update({'object_b': self.object_b})
        return data


class UrlHistoryView(DetailView):
    model = Url
    template_name = 'monitor/url_detail_history.html'


class ThambnailView(DetailView):
    model = UrlLog

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.
        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        im = base64.b64decode(self.object.screenshot)
        options = {'size': (self.kwargs.get('w', 320), self.kwargs.get('h', 200)), 'crop': True}
        img_temp = NamedTemporaryFile(delete=True, dir=os.path.join(settings.MEDIA_ROOT, 'thumbs'))
        img_temp.write(im)
        img_temp.flush()

        thumb = get_thumbnailer(Thumbnailer(img_temp)).get_thumbnail(options)

        return HttpResponse(thumb, content_type="image/png")
