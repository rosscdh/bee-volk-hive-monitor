# myapp/apps.py
from django.apps import AppConfig


class BoxConfig(AppConfig):
    name = 'beer.apps.box'

    def ready(self):
        from beer.apps.box.tasks import *

