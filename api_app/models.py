from django.db import models
from django.contrib.auth.models import User, UserManager

class ApiUser(User):
    """ The representation of a Api user """

    # fields
    token = models.CharField(max_length=30, default="", blank=True,
        help_text="A token that can be used to verify the user's email",
    )
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    class Meta:
        verbose_name_plural = "users"
