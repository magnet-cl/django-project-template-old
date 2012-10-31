""" This file contains some generic purpouse views """

from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import password_change as django_password_change
from base.forms import AuthenticationForm
from django.http import HttpResponse

def index(request):
    """ view that renders a default home"""
    return HttpResponse("Hello, world.")

def login(request):
    """ view that renders the login """
    # If the form has been submitted...
    return django_login(request, authentication_form=AuthenticationForm)

def password_change(request):
    """ view that renders the login """
    # If the form has been submitted...
    return django_password_change(request, post_change_redirect="/",
            template_name="registration/password_change.html")
