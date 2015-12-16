# -*- coding: utf-8 -*-
"""
Test the user can signup with a crazy none RFC valid email address
Test the user can signin with the same crazy email address
Note that the DB will save as valid ie.. Crap@NortyStuff.com will be saved as Crap@nortystuff.com
"""
import mock
from django.core import mail
from django.conf import settings
from django.core.urlresolvers import reverse

from model_mommy import mommy

from beer.tests.workflow_case import BaseScenarios

import re

"""
There is no signup form at the moment
"""
# class CustomerSignUpTest(BaseScenarios):
#     """
#     Specifically test the crazy uppercase lowercase domain
#     """
#     fixtures = ['dev-fixtures']  # load the demo matter from fixtures

#     def test_signup(self):
#         url = reverse('public:signup')
#         resp = self.client.get(url)

#         self.assertEqual(resp.context_data.get('form').fields.keys(), ['username', 'firm_name', 'first_name', 'last_name', 'email', 'password', 'password_confirm', 't_and_c', 'mpid'])

#         form_data = resp.context_data.get('form').initial
#         form_data.update({
#             'username': None,
#             'firm_name': 'Test Firm Inc.',
#             'first_name': 'Monkey',
#             'last_name': 'Tester',
#             'email': 'MySillyUserName@BadlyFormatedEmailNonRFCDomain.com',
#             'password': 'password',
#             'password_confirm': 'password',
#             't_and_c': True,
#             'csrfmiddlewaretoken': unicode(resp.context['csrf_token']),
#         })

#         form_resp = self.client.post(url, form_data, follow=True)

#         # is logged in
#         self.assertIn('_auth_user_id', self.client.session)
#         user = form_resp.context['user']
#         self.assertEqual(user.is_authenticated(), True)

#         # of this user
#         self.assertEqual(user.username, 'mysillyusername')
#         self.assertEqual(user.email, 'MySillyUserName@badlyformatedemailnonrfcdomain.com')

#         # redirected to DashView
#         self.assertEqual(type(form_resp.context_data.get('view')), MatterListView)

#         #
#         # Test that the users account is profile.validated_email = False
#         #
#         self.assertEqual(user.profile.validated_email, False)  # forces them to validate their email

#         outbox = mail.outbox

#         self.assertEqual(len(outbox), 1)
#         email = outbox[0]
#         self.assertEqual(email.recipients(), [u'MySillyUserName@badlyformatedemailnonrfcdomain.com'])
#         self.assertEqual(email.from_email, 'support@beer.com')
#         self.assertEqual(email.subject, 'Please confirm your email address')
#         self.assertTrue(re.search(r'/me/email_confirmed/(?P<token>.*)/', email.body))


class CustomerSignInTest(BaseScenarios):
    """
    Specifically test the crazy uppercase lowercase domain
    """
    def setUp(self):
        super(CustomerSignInTest, self).setUp()
        self.user = mommy.make('auth.User',
                               username='mysillyusername',
                               first_name='Monkey',
                               last_name='Tester',
                               email='MySillyUserName@badlyformatedemailnonrfcdomain.com')
        self.user.set_password('password')
        self.user.save()

    def test_signin(self):
        url = settings.LOGIN_URL
        resp = self.client.get(url)
        self.assertEqual(resp.context_data.get('form').fields.keys(), ['username', 'password'])

        form_data = resp.context_data.get('form').initial
        form_data.update({
            'username': 'MySillyUserName@BadlyFormatedEmailNonRFCDomain.com',
            'password': 'password',
        })

        form_resp = self.client.post(url, form_data, follow=True)

        # of this user
        self.assertEqual(form_resp.context['user'].is_authenticated(), True)
        self.assertEqual(form_resp.context['user'].username, 'mysillyusername')
        self.assertEqual(form_resp.context['user'].email, 'MySillyUserName@badlyformatedemailnonrfcdomain.com')
        # redirected to profile
        self.assertEqual(form_resp.redirect_chain, [('http://testserver/accounts/profile/', 302)])
