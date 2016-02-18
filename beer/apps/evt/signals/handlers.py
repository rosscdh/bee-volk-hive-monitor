# -*- coding: utf-8 -*-
from .base import log_bet_event, log_influx_event

from django.conf import settings
from django.dispatch import receiver

from pinax.eventlog.models import log
from requests.exceptions import ConnectionError


import arrow
import logging
import datetime
from influxdb import InfluxDBClient

logger = logging.getLogger('django.request')

influx_client = InfluxDBClient(settings.INFLUX_DB.get('host'),
                               settings.INFLUX_DB.get('port'),
                               settings.INFLUX_DB.get('username'),
                               settings.INFLUX_DB.get('password'),
                               settings.INFLUX_DB.get('database'))


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
    default_timestamp = arrow.utcnow().isoformat()

    sent_timestamp = kwargs.get('timestamp', default_timestamp)

    try:
        iso_format_timestamp = arrow.get(datetime.datetime.fromtimestamp(sent_timestamp)).isoformat()
    except ValueError:
        # as per http://stackoverflow.com/questions/10286224/javascript-timestamp-to-python-datetime-conversion sending timestamp with milliseconds
        iso_format_timestamp = arrow.get(datetime.datetime.fromtimestamp(sent_timestamp/1000)).isoformat()

    for metric in action.split(','):
        json_body.append({
            "measurement": metric,
            "tags": kwargs.get('tags', {}),
            "time": iso_format_timestamp,
            "fields": {
                "value": kwargs.get(metric)
            }
        })

    try:
        influx_client.write_points(json_body)
    except ConnectionError:
        logger.critical('Not able to conenct to InfluxDb')
