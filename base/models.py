# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""
# base
from base.managers import BaseManager

# django
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms.models import model_to_dict

# other
from django.utils import timezone

# standard library
import glob
import json
import os


class BaseModel(models.Model):
    """ An abstract class that every model should inherit from """
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

    def model_to_dict(self):
        # this uses the forms.models method 'model_to_dict'. This means that
        # all editable=False fields won't show up in the dictionary
        return model_to_dict(
            self,
            fields=[field.name for field in self._meta.fields]
        )

    def to_json(self):
        return json.dumps(self.model_to_dict(), cls=DjangoJSONEncoder)
