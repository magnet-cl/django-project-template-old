""" Admin page configuration for the api """
from django.contrib import admin

from base.models import User
from base.forms import UserCreationForm
from base.forms import UserChangeForm

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _


ERROR_MESSAGE = _("Please enter the correct email and password "
        "for a staff account. Note that both fields are case-sensitive.")

# we are going to override the email login
class AdminAuthenticationForm(admin.forms.AdminAuthenticationForm):
    """ Subclass which overrides the 'clean' method the email is accepted
    instead of the username

    """
    def clean(self):
        """ takes the email and password and authenticates with it """

        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data
admin.sites.AdminSite.login_form = AdminAuthenticationForm

#we are going to configure the user admin, so we first need to unregister
# the default one
admin.site.unregister(DjangoUser)


class UserAdmin(DjangoUserAdmin):
    """ Configuration for the User admin page"""
    add_form_template = 'admin/base/user/add_form.html'

    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                'password2')}
        ),
    )

admin.site.register(User, UserAdmin)
