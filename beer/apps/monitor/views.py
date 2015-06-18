# -*- coding: utf-8 -*-
from django.views.generic import DetailView

from .models import UrlLog, Url


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

