# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import signing

from rest_framework import status as http_status

from beer.tests import BaseObjectsTestCase


class VerifyUserRegistration(BaseObjectsTestCase):

    def setUp(self):
        super(VerifyUserRegistration, self).setUp()
        self.url = reverse('api:verify')
        self.token = signing.dumps(self.user.pk, salt=settings.URL_ENCODE_SECRET_KEY)

    def test_valid_verification(self):
        self.response = self.api.post(self.url, data={"token": self.token}, format='json')
        self.resp = self.response.data

        self.assertEqual(self.response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(self.resp.keys(), ['message'])
        self.assertEqual(self.resp['message'], u'User %s Validated' % self.user.email)

    def test_invalid_verification(self):
        self.response = self.api.post(self.url, data={"token": 'No token'}, format='json')
        self.resp = self.response.data

        self.assertEqual(self.response.status_code, http_status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.resp.keys(), ['detail'])
        self.assertEqual(self.resp['detail'], u'Not found')
