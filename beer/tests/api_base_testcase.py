import json

from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase, APIClient
from model_mommy import mommy

from beer.apps.role_permission.roles import ROLES, COMPANY_ROLES


class BaseObjectsTestCase(APITestCase):
    """
    Sets up base objects and provides test helpers for login etc
    """

    def setUp(self):
        # setup api object to interact with the api
        self.api = APIClient()

        # create the base user
        self.user = mommy.make('auth.User',
                               first_name='Tester',
                               last_name='One',
                               email='test+1@beer.com')
        self.user.set_password('password')

        # log them in
        self.api.force_authenticate(user=self.user)


class ApiViewsetWrapper():
    """
    Simple wrapper around the API to look up the standard routes and do a post/put/delete/get on them
    - Assumes the use of a viewsets.ModelViewSet
    - Use this in your test case __init__
    - self.api = ApiViewsetWrapper(self.api, "api:brand")  #  overwrite the BaseObjectTestCase self.api
    """

    def __init__(self, api, base_route):
        self.api = api
        self.base_route = base_route
        self.list_route = lambda: reverse(base_route + "-list")
        self.detail_route_by_name = lambda pk, route: reverse(base_route + "-" + route, args=(pk,))

    def _detail(self, pk, route_name=None):
        route_name = route_name if route_name else "detail"
        return reverse(self.base_route + "-" + route_name, args=(pk,))

    def post(self, data):
        resp = self.api.post(self.list_route(), data=data, format='json')
        return resp, resp.data

    def post_detail(self, pk, route_name, data=None):
        resp = self.api.post(self._detail(pk, route_name), data=data, format='json')
        return resp, resp.data

    def put(self, pk, data):
        resp = self.api.put(self._detail(pk), data=data, format='json')
        return resp, resp.data

    def patch(self, pk, data):
        resp = self.api.patch(self._detail(pk), data=data, format='json')
        return resp, resp.data

    def delete(self, pk, data):
        resp = self.api.delete(self._detail(pk), data=data, format='json')
        return resp, resp.data

    def list(self):
        resp = self.api.get(self.list_route(), format="json")
        return resp, resp.data

    def get(self, pk, route=None):
        resp = self.api.get(self._detail(pk, route))
        return resp, resp.data

    def force_authenticate(self, user):
        self.api.force_authenticate(user)

    @property
    def wrapped_api(self):
        return self.api
