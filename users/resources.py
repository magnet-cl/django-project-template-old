#!/usr/bin/python
# coding=utf-8
# vim: set fileencoding=utf-8 :
"""
This document defines the UserResource, which represents a user in the api.

"""
# standard library
import json
import logging

# django
from django.conf.urls import url
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError

# tastypie
from tastypie import fields
from tastypie import http
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.exceptions import Unauthorized
from tastypie.utils import trailing_slash

# utils

# api
from api.authentication import MethodWardAuthentication
from api.decorators import api_method
from api.decorators import required_fields
from api.resources import MultipartResource

# models
from users.models import User

# forms
from users.forms import UserForm

# Get an instance of a logger
logger = logging.getLogger('api.user')


class UserAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        # TODO implement permissions
        return True

    def create_list(self, object_list, bundle):
        raise Unauthorized("You don't have permissions to do this")

    def delete_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to delete the object in
        question or throw ``Unauthorized`` if they are not.
        """
        raise Unauthorized("You don't have permissions to do this")

    def update_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to update the object in
        question or throw ``Unauthorized`` if they are not.
        """
        if bundle.request.user.id != bundle.obj.id:
            raise Unauthorized("You don't have permissions to do this")

        return True


class UserResource(MultipartResource):
    """ Resource model for the User model """

    date_joined = fields.DateTimeField(
        'date_joined',
        readonly=True,
        help_text='When the user registered',
    )

    class Meta(MultipartResource.Meta):
        """ Metadata for the user resource """
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'post', 'patch']
        authentication = MethodWardAuthentication(
            annonymus_allowed_methods=['post']
        )
        authorization = UserAuthorization()

        excludes = [
            'password',
            'is_staff',
            'is_superuser',
            'is_active',
            'profile_picture',
        ]

        filtering = {
            'id': ALL,
            "division": ALL_WITH_RELATIONS,
            "business_line": ALL_WITH_RELATIONS,
        }

        extra_actions = [{
            "name": "is_authenticated",
            "http_method": "GET",
            "resource_type": "list",
            "summary": "Returns user data if he is authenticated",
            "fields": {
            }
        }, {
            "name": "current",
            "http_method": "GET",
            "resource_type": "list",
            "summary": "Returns user data if he is authenticated",
            "fields": {
            }
        }, {
            "name": "login",
            "http_method": "POST",
            "resource_type": "list",
            "summary": "Authenticates a user in the API.",
            "fields": {
                "rut": {
                    "type": "string",
                    "required": True,
                    "description": "The rut of the user"
                },
                "password": {
                    "type": "string",
                    "required": True,
                    "description": "The password of the user"
                }
            }
        }, {
            "name": "logout",
            "http_method": "DELETE",
            "resource_type": "list",
            "summary": "Logout endpoint",
            "fields": {
            }
        }, {
            "name": "recover_password",
            "http_method": "POST",
            "resource_type": "list",
            "summary": "Request a recover password email",
            "fields": {
                "email": {
                    "type": "string",
                    "required": True,
                    "description": "The email of the account to recover"
                }
            }
        }]

    def prepend_urls(self):
        """ Add the following array of urls to the UserResource base urls """
        resource_name = self._meta.resource_name
        return [
            # login
            url(r"^(?P<resource_name>%s)/login%s$" %
                (resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            # logout
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            # is_authenticated
            url(r'^(?P<resource_name>%s)/is_authenticated%s$' %
                (resource_name, trailing_slash()),
                self.wrap_view('authenticated'), name='api_authenticated'),
            # get curernt user
            url(r'^(?P<resource_name>%s)/current%s$' %
                (resource_name, trailing_slash()),
                self.wrap_view('get_current_user'),
                name='api_user_get_current_user'),
            # recover password
            url(r'^(?P<resource_name>%s)/recover_password%s$' %
                (resource_name, trailing_slash()),
                self.wrap_view('recover_password'),
                name='api_recover_password'),
        ]

    def authenticated(self, request, **kwargs):
        """ api method to check whether a user is authenticated or not"""

        try:
            return self.get_current_user(request, **kwargs)
        except ImmediateHttpResponse:
            # get current user throws an exception if there is no user
            return self.create_response(request, False)

    def get_current_user(self, request, **kwargs):
        """ api method to check whether a user is authenticated or not"""

        self.method_check(request, allowed=['get'])
        user = request.user
        if user.is_authenticated():

            bundle = self.build_bundle(obj=user, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)

            return self.create_response(request, bundle)

        response = http.HttpUnauthorized(
            json.dumps('No current user'),
            content_type=request.META.get('CONTENT_TYPE', 'application/json'))

        raise ImmediateHttpResponse(response=response)

    def recover_password(self, request, **kwargs):
        """ Sets a token to recover the password and sends an email with
        the token

        """

        # TODO: Handle users without email
        self.method_check(request, allowed=['post'])

        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json')
        )
        email = data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response = http.HttpBadRequest(
                json.dumps("User with email %s not found" % email),
                content_type=request.META['CONTENT_TYPE'])
            raise ImmediateHttpResponse(response=response)

        user.send_recover_password_email()

        return self.create_response(request, {'success': True})

    @api_method(single=True, expected_methods=['post'])
    def login(self, request, **kwargs):
        """ A new end point for login the user using the django login system

        """
        logger.debug('UserResource.login')

        logger.debug('UserResource.login: Content Type: '.format(
                     request.META.get('CONTENT_TYPE')))

        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json')
        )

        email = data.get('email', '')
        password = data.get('password', '')

        logger.debug('UserResource.login: email: {}'.format(email))

        user = authenticate(email=email, password=password)

        if user:
            logger.debug('UserResource.login: user found')

            if user.is_active:
                logger.debug('UserResource.login: login successful')
                login(request, user)
                return user
            else:
                logger.debug('UserResource.login: login fail, user not active')
                res = http.HttpForbidden(
                    json.dumps('disabled'),
                    content_type=request.META['CONTENT_TYPE'])
                raise ImmediateHttpResponse(response=res)
        else:
            res = http.HttpUnauthorized(
                json.dumps('invalid email or password'),
                content_type=request.META['CONTENT_TYPE'])
            raise ImmediateHttpResponse(response=res)

    def logout(self, request, **kwargs):
        """
        A new end point to logout the user using the django login system
        """
        self.method_check(request, allowed=['delete'])
        if request.user and request.user.is_authenticated():
            logout(request)

        return self.create_response(request, {'success': True})

    @required_fields(['email'])
    def obj_create(self, bundle, **kwargs):
        """
        Endpoint to create the user
        """

        if not bundle.request.user.is_authenticated():
            response = http.HttpUnauthorized(
                json.dumps("You don't have permissions to do this"),
                content_type=bundle.request.META['CONTENT_TYPE'])
            raise ImmediateHttpResponse(response=response)

        form = UserForm(bundle.data)

        if not form.is_valid():
            response = http.HttpBadRequest(
                json.dumps(form.errors),
                content_type=bundle.request.META['CONTENT_TYPE'])
            raise ImmediateHttpResponse(response=response)

        try:
            return super(UserResource, self).obj_create(bundle, **kwargs)
        except IntegrityError:
            response = http.HttpConflict(
                json.dumps("This email is already registered"),
                content_type=bundle.request.META['CONTENT_TYPE'])
            raise ImmediateHttpResponse(response=response)
