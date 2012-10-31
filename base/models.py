from django.db import models
from django.contrib.auth.models import User as DjangoUser, UserManager
import base64
import os


class BaseModel(models.Model):
    """ An abstract class that every model should inherit from """
    class Meta:
        """ set to abstract """
        abstract = True

    # public methods
    def update(self, **kwargs):
        """ proxy method for the QuerySet: update method
        highly recommended when you need to save just one field

        """
        self.__class__.objects.filter(pk=self.pk).update(**kwargs)


class User(DjangoUser, BaseModel):
    """ The representation of a Api user """

    # fields
    token = models.CharField(max_length=30, default="", blank=True,
        help_text="A token that can be used to verify the user's email",
    )
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def set_random_token(self):
        """ generate a random token """
        token = base64.urlsafe_b64encode(os.urandom(30))[:30]
        self.token = token
        self.save()
        return token

    class Meta:
        verbose_name_plural = "users"
