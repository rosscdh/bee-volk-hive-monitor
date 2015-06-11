# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^v1/docs/', include('rest_framework_swagger.urls')),
                       url(r'^v1/', include('beer.apps.api.urls', namespace='api')),
                       ) + static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
