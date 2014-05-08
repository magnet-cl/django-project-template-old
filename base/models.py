# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""
# base
from base.managers import BaseManager

# django
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# standard library
import json


class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.fields.files.FieldFile):
            if obj:
                return obj.url
            else:
                return None

        return super(ModelEncoder, self).default(obj)


class BaseModel(models.Model):
    """ An abstract class that every model should inherit from """
    BOOLEAN_CHOICES = ((False, _(u'No')), (True, _(u'Yes')))

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="creation date",
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True,
        help_text="edition date",
    )

    # using BaseManager
    objects = BaseManager()

    class Meta:
        """ set to abstract """
        abstract = True

    # public methods
    def update(self, **kwargs):
        """ proxy method for the QuerySet: update method
        highly recommended when you need to save just one field

        """
        kwargs['updated_at'] = timezone.now()

        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])

        self.__class__.objects.filter(pk=self.pk).update(**kwargs)

    def to_dict(instance, fields=None, exclude=None):
        """
        Returns a dict containing the data in ``instance``

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.
        """

        opts = instance._meta
        data = {}
        for f in opts.fields + opts.many_to_many:
            if fields and not f.name in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, models.fields.related.ManyToManyField):
                # If the object doesn't have a primary key yet, just use an
                # emptylist for its m2m fields. Calling f.value_from_object
                # will raise an exception.
                if instance.pk is None:
                    data[f.name] = []
                else:
                    # MultipleChoiceWidget needs a list of pks, not objects.
                    data[f.name] = list(
                        f.value_from_object(instance).values_list('pk',
                                                                  flat=True))
            else:
                data[f.name] = f.value_from_object(instance)
        return data

    def to_json(self, fields=None, exclude=None, **kargs):
        """
        Returns a string containing the data in of the instance in json format

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.

        kwargs are optional named parameters for the json.dumps method
        """
        # obtain a dict of the instance data
        data = self.to_dict(fields=fields, exclude=exclude)

        # turn the dict to json
        return json.dumps(data, cls=ModelEncoder, **kargs)
