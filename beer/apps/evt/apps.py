# myapp/apps.py
from django.apps import AppConfig


class EvtConfig(AppConfig):
    name = 'beer.apps.evt'

    def ready(self):
        from beer.apps.evt.signals.handlers import _log_bet_event, _log_influx_event

