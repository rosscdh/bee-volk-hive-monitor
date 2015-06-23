# -*- coding: utf-8 -*-
from django.core import mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import signing

from rest_framework import status as http_status

from beer.tests import BaseObjectsTestCase
from django.contrib.auth.models import User


class RegisterBrandCompanyViewTest(BaseObjectsTestCase):
    """
    Test the Brand View returns only the logged in users brands
    """
    company_type = 'brand_owner'
    expected_role = User.ROLES.get_name_by_value(User.ROLES.brand_account_admin)

    def setUp(self):
        super(RegisterBrandCompanyViewTest, self).setUp()
        self.url = reverse('api:register')
        mail.outbox = []

    def test_registration(self):
        """
        """
        data = {
            "first_name": "Test",
            "last_name": "Monkey",
            "email": "test+monkey@beer.com",
            "password": "test"
        }
        self.response = self.api.post(self.url, data=data, format='json')
        self.resp = self.response.data

        self.assertEqual(self.resp['role'], self.expected_role)
        outbox = mail.outbox
        self.assertEqual(outbox[0].subject, 'Welcome to beer')
        # standard url
        self.assertTrue('/me/email_confirmed/' in outbox[0].body)

    def test_custom_client_activiation_link_registration(self):
        """
        """
        expected_activation_link = "http://my_awesome_site.com/user/verify/:token"  # NOTE this is the format!
        data = {
            "activation_link": expected_activation_link,
            "first_name": "Test",
            "last_name": "Monkey",
            "email": "test+monkey@beer.com",
            "password": "test"
        }
        self.response = self.api.post(self.url, data=data, format='json')
        self.resp = self.response.data

        self.assertEqual(self.resp['role'], self.expected_role)
        outbox = mail.outbox

        self.assertEqual(outbox[0].subject, 'Welcome to beer')
        expected_activation_link = expected_activation_link.replace(':token', '')
        self.assertTrue(expected_activation_link in outbox[0].body)

    def test_existing_company_registration_invalid(self):
        """
        """
        data = {
            "first_name": "Test",
            "last_name": "Monkey",
            "email": "test+monkey@beer.com",
            "password": "test"
        }
        self.response = self.api.post(self.url, data=data, format='json')
        self.resp = self.response.data

        self.assertEqual(self.response.status_code, http_status.HTTP_406_NOT_ACCEPTABLE)

        self.assertEqual(self.resp['error'], u'The company: %s already exists, please ask the admin registrant to invite you' % self.company.name)


class RegisterPrintingPartnerCompanyViewTest(RegisterBrandCompanyViewTest):
    company_type = 'printing_partner'
    expected_role = User.ROLES.get_name_by_value(User.ROLES.printer_account_admin)


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
