""" This document defines the UserManager class"""

from django.contrib.auth.models import UserManager as DjangoUserManager
from base.managers import BaseManager


class UserManager(DjangoUserManager, BaseManager):
    """
    This class is used so the user manager has both the django defined
    user manager and the cusmtom defiled 'BaseManager
    ""
    """
    pass
