""" This file contains some generic purpouse views """

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import password_change as django_password_change
from base.forms import AuthenticationForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect

@login_required
def index(request):
    """ view that renders a default home"""
    return HttpResponse("Hello, world.")

def login(request):
    """ view that renders the login """
    # If the form has been submitted...
    return django_login(request, authentication_form=AuthenticationForm)

def logout(request):
    """ view that handles the logout """
    django_logout(request)
    return HttpResponseRedirect('/')

def password_change(request):
    """ view that renders the login """
    # If the form has been submitted...
    return django_password_change(request, post_change_redirect="/",
            template_name="registration/password_change.html")
