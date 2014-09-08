# api
from api.urls import api

# django
from django.test import Client

# tasypie
from tastypie.test import ResourceTestCase
from tastypie.test import TestApiClient

from users.resources import UserResource
from locations.resources import LocationResource

# tests
from base.tests import BaseTestCase

# standard library
import json


class BaseResourceTestCase(BaseTestCase, ResourceTestCase):

    def setUp(self):
        super(BaseResourceTestCase, self).setUp()
        self.user_resource = UserResource()
        self.user_resource_uri = self.user_resource.get_resource_uri()

        self.client = TestApiClient()

        # login
        self.password = 'superpassword'
        self.user.set_password(self.password)
        self.user.save()
        self.login(self.user.email, self.password)

        self.location_resource = LocationResource()
        self.location_resource_uri = self.location_resource.get_resource_uri()

    def login(self, email=None, password=None):
        if email is None:
            email = self.user.email

        if password is None:
            password = self.password

        url = "%slogin/" % self.user_resource_uri
        data = {
            "email": email,
            "password": password,
        }

        if isinstance(self.client, Client):
            data = json.dumps(data)

        response = self.client.post(url, data=data,
                                    content_type="application/json")

        self.assertEqual(
            response.status_code, 200,
            "On '{}', expected status code: {}. Got {}: {}".format(
                url,
                200,
                response.status_code,
                response.content
            )
        )

    def logout(self):
        uri = "%slogout/" % self.user_resource_uri
        data = {
        }

        response = self.client.get(uri, data=data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def create(self, resource, endpoint='', expected_code=201, **data):
        return self.post(resource, expected_code=expected_code, **data)

    def get(self, *args, **kwargs):
        return self.call_api(method='get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.call_api(method='post', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.call_api(method='put', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.call_api(method='patch', *args, **kwargs)

    def call_api(self, resource, obj=None, endpoint='', expected_code=200,
                 data=None, method='get', multipart=False):

        if multipart:
            self.client = Client()
            self.login()

        if isinstance(resource, basestring):
            resource = api.canonical_resource_for(resource)

        url = resource.get_resource_uri(obj)

        if endpoint:
            url = '{}{}/'.format(url, endpoint)

        method = getattr(self.client, method.lower())

        response = method(url, data=data)

        self.assertEqual(
            response.status_code, expected_code,
            "On '{}', expected status code: {}. Got {}: {}".format(
                url,
                expected_code,
                response.status_code,
                response.content
            )
        )

        try:
            return json.loads(response.content)
        except:
            return response.content
