""" Admin page configuration for the api """
from django.contrib import admin

from api_app.models import User

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _


ERROR_MESSAGE = _("Please enter the correct email and password "
        "for a staff account. Note that both fields are case-sensitive.")

#we are going to configure the user admin, so we first need to unregister
# the default one
admin.site.unregister(DjangoUser)


class UserAdmin(DjangoUserAdmin):
    """ Configuration for the User admin page"""

admin.site.register(User, UserAdmin)
