# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from beer.tests import BaseObjectsTestCase


class ApiRolesEndpointTest(BaseObjectsTestCase):
    """
    Test the Roles endpoint
    """

    def test_roles_endpoint(self):
        """
        """
        url = reverse('api:roles')
        response = self.api.get(url)
        resp = response.data

        self.assertEqual(type(resp), list)
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp[0].keys(), ['permissions', 'id', 'name', 'slug'])
