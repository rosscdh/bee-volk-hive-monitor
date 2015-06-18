from django.contrib import admin

from .models import Url, UrlLog, MonitorSite

admin.site.register([Url, UrlLog, MonitorSite])
