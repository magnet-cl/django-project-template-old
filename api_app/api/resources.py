""" This document defines the resources for the API"""

from api_app.models import ApiUser
from datetime import datetime
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastytools import fields
from tastytools.api import Api
from tastytools.authentication import AuthenticationByMethod
from tastytools.resources import ModelResource


class ApiResource(ModelResource):
    """ the base class of every Api Resource """
    class Meta:
        """ Metadata for the Api resource """
        always_return_data = True


class UserResource(ApiResource):
    """ Resource model for the User model """
    email = fields.CharField('email', null=True, blank=True,
            help_text="The contact email for this user")
    first_name = fields.CharField('first_name', null=True, blank=True,
            help_text="The first name of this user")
    last_name = fields.CharField('last_name', null=True, blank=True,
            help_text="The last name of this user")
    last_login = fields.DateTimeField('last_login', default=datetime.now,
            help_text="The date of the lat login for this user")

    class Meta(ApiResource.Meta):
        """ Metadata for the user resource """
        queryset = ApiUser.objects.all()
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

api = Api(api_name='resources')
api.register(UserResource())
