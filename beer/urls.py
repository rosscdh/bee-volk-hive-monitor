# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       # Auth with JWT
                       url(r'^auth/token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
                       url(r'^auth/token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),

                       # User Auth
                       url(r'^rest-auth/', include('rest_auth.urls')),
                       url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))

                       url(r'^v1/docs/', include('rest_framework_swagger.urls')),
                       url(r'^v1/', include('beer.apps.api.urls', namespace='api')),
                       ) + static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
