# -*- coding: utf-8 -*-
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from model_mommy import mommy
from pyquery import PyQuery as pq

from .api_base_testcase import BaseObjectsTestCase

import json
import logging
import datetime
logger = logging.getLogger('django.test')


class PyQueryMixin(object):
    """
    Base mixin for using PyQuery for response.content selector lookups
    https://pypi.python.org/pypi/pyquery
    """
    def setUp(self):
        super(PyQueryMixin, self).setUp()
        self.pq = pq


class BaseScenarios(PyQueryMixin, BaseObjectsTestCase, TestCase):
    fixtures = 'sites test_clients test_products test_codes test_users'
    password = 'password'

    def login(self, user):
        self.client.login(username=user.email, password=self.password)

    def create_user(self, username, email, user_class='customer', **extra_fields):
        User = get_user_model()
        client = extra_fields.pop('client', self.workspace_client)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = mommy.make('auth.User', username=username, email=email, client=client, **extra_fields)
            user.set_password(self.password)
            user.save()

        profile = user.profile
        profile.validated_email = True
        profile.save(update_fields=['data'])

        return user
