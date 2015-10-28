# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import receiver

from pinax.eventlog.models import log

import arrow
from influxdb import InfluxDBClient

influx_client = InfluxDBClient(settings.INFLUX_DB.get('host'),
                               settings.INFLUX_DB.get('port'),
                               settings.INFLUX_DB.get('username'),
                               settings.INFLUX_DB.get('password'),
                               settings.INFLUX_DB.get('database'))

from .base import log_bet_event, log_influx_event

import datetime


@receiver(log_bet_event)
def _log_bet_event(sender, signal, action, *args, **kwargs):
    """
    Log a custom event
    """
    log(action=action.lower().strip(),
        user=kwargs.pop('user', None),
        dateof=datetime.datetime.utcnow(),
        extra=kwargs)



@receiver(log_influx_event)
def _log_influx_event(sender, signal, action, *args, **kwargs):
    """
    Log a custom event
    """
    json_body = []
    for action in action.split(','):
        json_body.append({
            "measurement": action,
            "tags": kwargs.get('tags', {}),
            "time": arrow.utcnow().isoformat(),
            "fields": {
                "value": kwargs.get(action)
            }
        })
    influx_client.write_points(json_body)
