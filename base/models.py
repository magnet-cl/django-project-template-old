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
from base.image import generate_thumbnail
from PIL import Image
from PIL import ImageFile

# standard library
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

    def _process_image(self, field_name, image_sizes=None):
        field = getattr(self, field_name)

        if image_sizes is None:
            image_sizes = self.image_sizes

        try:
            file_path = field.file.name
        except ValueError:
            pass
        except IOError:
            return
        else:
            path = file_path.split('.')
            extension = path[-1]

            if extension != 'jpg':

                ImageFile.LOAD_TRUNCATED_IMAGES = True

                im = Image.open(file_path)
                path[-1] = 'jpg'
                final_path = ".".join(path)
                im = im.convert('RGB')
                im.save(final_path, 'JPEG')
                name = self.file_path(os.path.basename(final_path))
                self.update(**{field_name: name})
                try:
                    if im.fp:
                        im.fp.close()
                except:
                    pass

                file_path = final_path

            for size in image_sizes:
                generate_thumbnail(file_path, size)
