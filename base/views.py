# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

from base.forms import AuthenticationForm
from base.forms import UserCreationForm
from base.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

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
    success_url = "/accounts/reset/done/"

    return auth_views.password_reset_confirm(request, uidb36, token,
                                             template_name=template_name,
                                             post_reset_redirect=success_url)

def password_reset_complete(request):
    """ view that handles the recover password process """

    template_name = "accounts/password_reset_complete.html"
    return auth_views.password_reset_complete(request,
                                              template_name=template_name)

def user_new(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(verify_email_address=True, request=request)
            messages.add_message(request, messages.INFO,
                                 _("An email has been sent to you. Please "
                                    "check it to veiry your email."))
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
    }

    return render_to_response('accounts/user_new.html', context,
                              context_instance=RequestContext(request))

# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(request, uidb36=None, token=None,
                     token_generator=default_token_generator,
                     current_app=None, extra_context=None):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """

    assert uidb36 is not None and token is not None # checked by URLconf
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(request, messages.INFO,
                             _("Your email address has been verified."))
    else:
        messages.add_message(request, messages.ERROR,
                             _("Invalid verification link"))

    return HttpResponseRedirect(reverse('login'))

