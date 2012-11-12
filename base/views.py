""" This file contains some generic purpouse views """

from base.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

@login_required
def index(request):
    """ view that renders a default home"""
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def login(request):
    """ view that renders the login """
    # If the form has been submitted...
    template_name = "accounts/login.html"
    return django_login(request, authentication_form=AuthenticationForm,
                        template_name=template_name)

def logout(request):
    """ view that handles the logout """
    django_logout(request)
    return HttpResponseRedirect('/')

@login_required
def password_change(request):
    """ view that renders the login """
    # If the form has been submitted...
    template_name = "accounts/password_change.html"

    return auth_views.password_change(request, post_change_redirect="/",
                                      template_name=template_name)

def password_reset(request):
    """ view that handles the recover password process """

    template_name = "accounts/password_reset_form.html"
    email_template_name = "emails/password_reset.html"

    success_url = "/accounts/password_email_sent"

    res = auth_views.password_reset(request,
                                    post_reset_redirect=success_url,
                                    template_name=template_name,
                                    email_template_name=email_template_name)
    return res

def password_reset_email_sent(request):
    messages.add_message(request, messages.INFO,
                         _("An email has been sent to you. Please check it "
                           "to reset your password."))
    return HttpResponseRedirect('/')

def password_reset_confirm(request, uidb36, token):
    """ view that handles the recover password process """
    template_name = "accounts/password_reset_confirm.html"
    return auth_views.password_reset_confirm(request, uidb36, token,
                                             template_name=template_name)

def password_reset_complete(request):
    """ view that handles the recover password process """

    template_name = "accounts/password_reset_complete.html"
    return auth_views.password_reset_complete(request,
                                              template_name=template_name)
