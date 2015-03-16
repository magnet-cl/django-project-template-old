"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# django
from django.db import models
from django.test import TestCase
from django.utils import timezone

# models
from users.models import User

# standard library
import random
import string
import re
import inspect


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

    def random_string(self, length=6):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(length))

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)


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

        for attr_name, attr in globals().items():
            if inspect.isclass(attr) and issubclass(attr, models.Model):

                # name change to increase test readability
                model = attr
                obj, related_nullable_objects = self.create_full_object(model)

                obj_count = model.objects.count()

                for relation_name, obj in related_nullable_objects.items():
                    obj.delete()

                    error_msg = (
                        '<{}> object, was deleted after deleting a nullable '
                        'related <{}> object, the relation was {}'
                    ).format(model.__name__, obj.__class__.__name__,
                             relation_name)

                    self.assertEqual(obj_count, model.objects.count(),
                                     error_msg)
