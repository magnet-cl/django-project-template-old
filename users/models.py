# -*- coding: utf-8 -*-
""" Models for the users application.

All apps should use the users.User model for all users
"""
# managers
from users.managers import UserManager

# models
from base.models import BaseModel

# django
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.db import models
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

# standard library
from threading import Thread
import base64
import os
import time

# base
from base import utils

# mark for translation the app name
ugettext_noop("Users")


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    User model with admin-compliant permissions, and BaseModel characteristics

    Email and password are required. Other fields are optional.
    """

    # required fields
    email = models.EmailField(
        _('email address'), unique=True, db_index=True,
        help_text=_("An email address that identifies this user")
    )
    # optional fields
    first_name = models.CharField(
        _('first name'), max_length=30, blank=True,
        help_text=_("The first name of this user"),
    )
    last_name = models.CharField(
        _('last name'), max_length=30, blank=True,
        help_text=_("The last name of this user"),
    )
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),
    )
    # auto fields
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now,
        help_text=_("The date this user was created in the database"),
    )
    token = models.CharField(
        max_length=30, default="", blank=True,
        help_text="A token that can be used to verify the user's email"
    )
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # django user methods
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    # custom methods
    def set_random_token(self):
        """ generate a random token """
        token = base64.urlsafe_b64encode(os.urandom(30))[:30]
        self.token = token
        self.save()
        return token

    # public methods
    def save(self, *args, **kwargs):
        """ store all emails in lowercase """
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

    def send_email(self, template_name, subject, template_vars={},
                   fail_silently=True, headers=None):
        """
        Sends an email to the registered address using a given template name
        """
        try:
            kwargs = {
                'email_list': [self.email],
                'template_name': template_name,
                'subject': subject,
                'template_vars': template_vars,
                'fail_silently': fail_silently,
                'headers': headers,
            }
            t = Thread(target=User.send_email_to, kwargs=kwargs)
            t.start()
        except Exception, error:
            if settings.DEBUG:
                print str(error)

    def send_example_email(self):
        """
        Sends an email to test the email funcionality.
        """
        title = _("Hello")
        template = "example_email"

        template_vars = {
            'user': self,
        }
        self.send_email(template, title, template_vars, fail_silently=False)

    # static methods
    @staticmethod
    def send_email_to(email_list, template_name, subject, sender=None,
                      template_vars=None, fail_silently=True,
                      attachments=None, headers=None):
        """ Sends an email to a list of emails using a given template name """

        if template_vars is None:
            template_vars = {}

        if attachments is None:
            attachments = []

        if not settings.ENABLE_EMAILS:
            return

        text_template = get_template("emails/%s.txt" % template_name)
        html_template = get_template("emails/%s.html" % template_name)
        context = Context(template_vars)

        text_content = text_template.render(context)
        html_content = html_template.render(context)

        sender = "%s <%s>" % (settings.EMAIL_SENDER_NAME,
                              settings.SENDER_EMAIL)

        emails_in_groups_of_5 = utils.grouper(email_list, 5)

        for emails in emails_in_groups_of_5:
            msg = EmailMultiAlternatives(subject, text_content,
                                         sender, emails, headers=headers)

            for attachment in attachments:
                attachment.seek(0)
                msg.attach(attachment.name, attachment.read(),
                           'application/pdf')

            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send(fail_silently=fail_silently)
            except:
                time.sleep(1)
                msg.send(fail_silently=fail_silently)
