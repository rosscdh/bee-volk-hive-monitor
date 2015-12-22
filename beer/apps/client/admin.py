# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner')
    search_fields = ('name', 'slug', 'owner__first_name', 'owner__last_name')

    def get_queryset(self, request):
        return super(ClientAdmin, self).get_queryset(request=request).select_related('owner')


# admin.site.register(Client, ClientAdmin)


