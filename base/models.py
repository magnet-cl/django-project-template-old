# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User as DjangoUser, UserManager
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from threading import Thread

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
        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])
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

    #static methods
    @staticmethod
    def send_email_to(email_list, template_name, subject,
            template_vars={}, fail_silently=True):
        """ Sends an email to a list of emails using a given template name """

        text_template = get_template("emails/%s.txt" % template_name)
        html_template = get_template("emails/%s.html" % template_name)
        context = Context(template_vars)

        text_content = text_template.render(context)
        html_content = html_template.render(context)

        sender = "%s <%s>" % (settings.EMAIL_SENDER_NAME,
                              settings.SENDER_EMAIL)
        msg = EmailMultiAlternatives(subject, text_content,
            sender, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=fail_silently)

    #private methods
    def _send_email(self, template_name, subject, template_vars={},
            fail_silently=True):
        """Sends an email to the registered address using a given template
        name

        """
        template_vars.update({'profile': self})
        User.send_email_to(
            email_list=[self.email],
            template_name=template_name,
            subject=subject,
            template_vars=template_vars,
            fail_silently=fail_silently,
        )

    #public methods
    def send_email(self, template_name, subject, template_vars=None,
            fail_silently=True):
        """Sends an email to the registered address using a given template
        name

        """
        try:
            t = Thread(target=self._send_email, args=(template_name, subject,
                template_vars, fail_silently))
            t.start()
        except Exception, error:
            if settings.DEBUG:
                print str(error)

    def send_example_email(self):
        """ Sends an email with the required token so a user can recover his/her
        password

        """
        title = _("Hello")
        template = "example_email"

        template_vars = {
            'user': self,
        }
        self.send_email(template, title, template_vars, fail_silently=False)
