# -*- coding: utf-8 -*-
from django.test import TestCase

from .api_base_testcase import BaseObjectsTestCase
from .workflow_case import BaseScenarios


class BaseEndpointTest(BaseScenarios, TestCase):
    """
    """
    endpoint = None

    def test_endpoint_name(self):
        self.assertEqual(self.endpoint, None)
