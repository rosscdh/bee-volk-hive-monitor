# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase, APIClient

from model_mommy import mommy


class BaseObjectsTestCase(APITestCase):
    """
    Sets up base objects and provides test helpers for login etc
    """
    fixtures = ('monitor.json',)

    def setUp(self):
        # setup api object to interact with the api
        self.api = APIClient()
