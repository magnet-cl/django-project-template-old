""" This file contains some generic purpouse views """

from django.contrib.auth.views import login as django_login
from base.forms import AuthenticationForm


def login(request):
    """ view that renders the login """
    # If the form has been submitted...
    return django_login(request, authentication_form=AuthenticationForm)
