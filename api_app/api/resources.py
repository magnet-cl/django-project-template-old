""" This document defines the resources for the API"""

from api_app.models import User
from datetime import datetime
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastytools import fields
from tastytools.api import Api
from tastytools.authentication import AuthenticationByMethod
from tastytools.resources import ModelResource

import json


class ApiResource(ModelResource):
    """ the base class of every Api Resource """
    class Meta:
        """ Metadata for the Api resource """
        always_return_data = True
    def override_urls(self):
        print "holi"
        return False


class UserResource(ApiResource):
    """ Resource model for the User model """
    email = fields.CharField('email', null=True, blank=True,
            help_text="The contact email for this user")
    first_name = fields.CharField('first_name', null=True, blank=True,
            help_text="The first name of this user")
    last_name = fields.CharField('last_name', null=True, blank=True,
            help_text="The last name of this user")
    last_login = fields.DateTimeField('last_login', default=datetime.now,
            help_text="The date of the last login for this user")
    date_joined = fields.DateTimeField('date_joined', default=datetime.now,
        help_text="The date when this user joined the app")

    class Meta(ApiResource.Meta):
        """ Metadata for the user resource """
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'put', 'post']
        authentication = AuthenticationByMethod('POST')
        authorization = Authorization()

        excludes = [
            'password',
            'is_staff',
            'is_superuser',
        ]
        filtering = {
            'username': ALL,
            'id': ALL,
        }

    def obj_create(self, bundle, request=None, **kwargs):
        self.is_valid(bundle, request)

        if bundle.errors:
            self.error_response(bundle.errors, request)

        required_list = [
            'email',
            'first_name',
            'last_name',
        ]

        for required_field in required_list:
            if required_field not in bundle.data:
                response = HttpBadRequest(
                        json.dumps("missing %s field" % required_field),
                        content_type=request.META['CONTENT_TYPE'])
                raise ImmediateHttpResponse(response=response)

        return super(UserResource, self).obj_create(
            bundle, request, user=request.user, **kwargs)

api = Api(api_name='resources')
api.register(UserResource())
