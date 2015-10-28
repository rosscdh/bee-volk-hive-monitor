# -*- coding: utf-8 -*-
import django.dispatch


log_bet_event = django.dispatch.Signal(providing_args=['sender', 'action'])
log_influx_event = django.dispatch.Signal(providing_args=['sender', 'action'])