from django.contrib.auth.hashers import check_password
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from beer.tests import BaseObjectsTestCase


class ChangePasswordApiTest(BaseObjectsTestCase):
    def setUp(self):
        super(ChangePasswordApiTest, self).setUp()
        self.url = reverse('api:change-password')

    def test_current_password_must_be_correct(self):
        resp = self.api.post(self.url, data={
            'old_password': 'blah',
            'new_password': 'eft',
            'confirm_new_password': 'efg'
        }, format='json')
        self.assertEqual(400, resp.status_code)
        self.assertTrue('old_password' in resp.data)
        self.assertEqual(['Current password is incorrect.'], resp.data['old_password'])

    def test_password_changes(self):
        resp = self.api.post(self.url, data={
            'old_password': 'password',
            'new_password': 'abc',
            'confirm_new_password': 'abc'
        }, format='json')
        self.assertEqual(resp.status_code, 200)

        u = User.objects.get(pk=self.user.pk)
        self.assertTrue(check_password('abc', u.password))

    def test_validation_fails_if_passwords_no_match(self):
        resp = self.api.post(self.url, data={
            'old_password': 'password',
            'new_password': 'eft',
            'confirm_new_password': 'efg'
        }, format='json')
        data = resp.data
        self.assertEqual(resp.status_code, 400)
        self.assertTrue("confirm_new_password" in data)
        self.assertEqual([u"Passwords do not match."], data["confirm_new_password"])


    def test_confirm_pwd_error_message_shows_required(self):
        # testing that the error message is the "required" error message, not the "do not match" error message"
        resp = self.api.post(self.url, data={
            'old_password': 'password',
            'new_password': 'eft',
        }, format='json')
        data = resp.data
        self.assertEqual(resp.status_code, 400)
        self.assertTrue("confirm_new_password" in data)
        self.assertEqual([u"This field is required."], data["confirm_new_password"])