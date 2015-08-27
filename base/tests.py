"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# standard library
import random
import string
import re
import os

# django
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import get_models
from django.test import TestCase
from django.utils import timezone

# models
from users.models import User

# urls
from project.urls import urlpatterns


def camel_to_underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def underscore_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        self.password = self.random_string()
        self.user = self.create_user(self.password)

        self.login()

    def create_user(self, password=None, **kwargs):
        if kwargs.get('first_name') is None:
            kwargs['first_name'] = self.random_string(length=6)

        if kwargs.get('last_name') is None:
            kwargs['last_name'] = self.random_string(length=6)

        if kwargs.get('email') is None:
            kwargs['email'] = "%s@gmail.com" % self.random_string(length=6)

        if kwargs.get('is_active') is None:
            kwargs['is_active'] = True

        user = User.objects.create(**kwargs)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def login(self, user=None, password=None):
        if user is None:
            user = self.user
            password = self.password

        return self.client.login(email=user.email, password=password)

    def random_email(self):
        return "{}@{}.{}".format(
            self.random_string(length=6),
            self.random_string(length=6),
            self.random_string(length=2)
        )

    def random_int(self, minimum=-100000, maximum=100000):
        return random.randint(minimum, maximum)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)

    def random_string(self, length=6, chars=None):
        if chars is None:
            chars = string.ascii_uppercase + string.digits

        return ''.join(random.choice(chars) for x in range(length))

    def set_required_boolean(self, data, field, **kwargs):
        if field not in data:
            data[field] = not not random.randint(0, 1)

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_rut(self, data, field, length=6):
        if field not in data:
            rut = '{}.{}.{}-{}'.format(
                self.random_int(minimum=1, maximum=99),
                self.random_int(minimum=100, maximum=990),
                self.random_int(minimum=100, maximum=990),
                self.random_string(length=1, chars='k' + string.digits),
            )
            data[field] = rut

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))


class IntegrityOnDeleteTestCase(BaseTestCase):
    def create_full_object(self, model):
        kwargs = {}
        for f in model._meta.fields:
            if isinstance(f, models.fields.related.ForeignKey) and f.null:
                model_name = camel_to_underscore(f.rel.to.__name__)
                method_name = 'create_{}'.format(model_name)
                kwargs[f.name] = getattr(self, method_name)()

        method_name = 'create_{}'.format(camel_to_underscore(model.__name__))

        return getattr(self, method_name)(**kwargs), kwargs

    def test_integrity_on_delete(self):

        for model in get_our_models():
            obj, related_nullable_objects = self.create_full_object(model)

            obj_count = model.objects.count()

            for relation_name, rel_obj in related_nullable_objects.items():

                try:
                    # check if the test should be skipped
                    if relation_name in obj.exclude_on_on_delete_test:
                        continue
                except AttributeError:
                    pass

                rel_obj.delete()

                error_msg = (
                    '<{}> object, was deleted after deleting a nullable '
                    'related <{}> object, the relation was "{}"'
                ).format(model.__name__, rel_obj.__class__.__name__,
                         relation_name)

                self.assertEqual(obj_count, model.objects.count(), error_msg)

            # feedback that the test passed
            print '.',


def get_our_models():
    for model in get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


def reverse_pattern(pattern, namespace, args=None, kwargs=None):
    try:
        if namespace:
            return reverse('{}:{}'.format(
                namespace, pattern.name, args=args, kwargs=kwargs)
            )
        else:
            return reverse(pattern.name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None


class UrlsTest(BaseTestCase):

    def setUp(self):
        super(UrlsTest, self).setUp()

        # we are going to send parameters, so one thing we'll do is to send
        # tie id 1
        self.user.delete()
        self.user.id = 1
        self.user.save()
        self.login()

        self.default_params = {}

        for model in get_our_models():
            model_name = camel_to_underscore(model.__name__)
            method_name = 'create_{}'.format(model_name)
            param_name = '{}_id'.format(model_name)

            obj = getattr(self, method_name)()

            self.assertIsNotNone(obj, '{} returns None'.format(method_name))

            self.default_params[param_name] = obj.id

    def reverse_pattern(self, pattern, namespace):
        url = reverse_pattern(pattern, namespace)

        if url is None:
            reverse_pattern(pattern, namespace, args=(1,))

            if url is None:
                reverse_pattern(pattern, namespace, args=(1, 1))

        if url is None:
            return None

        view_params = resolve(url).kwargs

        for param in view_params:
            try:
                view_params[param] = self.default_params[param]
            except KeyError:
                pass

        return reverse_pattern(pattern, namespace, kwargs=view_params)

    def test_responses(self):

        def test_url_patterns(patterns, namespace=''):

            ignored_namespaces = ['tastypie_swagger', 'djdt']

            if namespace in ignored_namespaces:
                return

            for pattern in patterns:
                self.login()

                if hasattr(pattern, 'name'):
                    url = self.reverse_pattern(pattern, namespace)

                    if not url:
                        continue

                    try:
                        response = self.client.get(url)
                    except:
                        print "Url {} failed: ".format(url)
                        raise

                    msg = 'url "{}" returned {}'.format(
                        url, response.status_code
                    )
                    self.assertIn(
                        response.status_code,
                        (200, 302, 403), msg
                    )
                    # feedback that the test passed
                    print '.',
                else:
                    test_url_patterns(pattern.url_patterns, pattern.namespace)

        test_url_patterns(urlpatterns)

        for model, model_admin in admin.site._registry.items():
            patterns = model_admin.get_urls()
            test_url_patterns(patterns, namespace='admin')
