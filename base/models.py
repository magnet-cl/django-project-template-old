# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""
# base
from base.managers import BaseManager

# django
from django.conf import settings
from django.db import models

# other
from django.utils import timezone


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

    def get_image_url(self, field_name="picture", width=None, height=None):
        """ returns the url of an image stored in the attribute with the name
        field_name and with the size specified by width and height
        """

        if width and height:
            file_path = "{}{}x{}/{}".format(
                settings.MEDIA_URL, width, height, str(self.picture))
        else:
            file_path = "{}{}".format(settings.MEDIA_URL,  str(self.picture))

        return file_path
