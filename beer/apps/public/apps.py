# myapp/apps.py
from django.apps import AppConfig


class BeerDefaultConfig(AppConfig):
    name = 'beer.apps.public'

    def ready(self):
        pass

