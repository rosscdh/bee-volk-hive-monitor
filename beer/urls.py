# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       # User Auth
                       url(r'^auth/token/', 'rest_framework_jwt.views.obtain_jwt_token'),
                       url(r'^auth/token/refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
                       url(r'^auth/', include('rest_auth.urls')),
                       url(r'^auth/registration/', include('rest_auth.registration.urls')),
                       url(r'^accounts/', include('allauth.urls')),

                       url(r'^v1/docs/', include('rest_framework_swagger.urls')),
                       url(r'^v1/', include('beer.apps.api.urls', namespace='api')),

                       url(r'^', include('django.contrib.auth.urls')),
                       url(r'^', include('beer.apps.payment_plans.urls', namespace='payment_plans')),

                       ) + static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
