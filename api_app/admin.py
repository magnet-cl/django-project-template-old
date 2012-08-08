""" Admin page configuration for the api """
from django.contrib import admin

from api_app.models import ApiUser

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


ERROR_MESSAGE = _("Please enter the correct email and password "
        "for a staff account. Note that both fields are case-sensitive.")

#we are going to configure the user admin, so we first need to unregister
# the default one
admin.site.unregister(User)


class ApiUserAdmin(UserAdmin):
    """ Configuration for the User admin page"""

admin.site.register(ApiUser, ApiUserAdmin)
