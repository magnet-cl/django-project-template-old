""" Admin page configuration for the api """
from django.contrib import admin

from base.models import User

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
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


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(label=_("E-mail"), max_length=75,
        help_text=_("Enter the same password as above, for verification."),
    )
    first_name = forms.CharField(label=_("First name"),
        help_text=_("The name of the user"),
    )
    last_name = forms.CharField(label=_("Last name"),
        help_text=_("The last name of the user"),
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput, required=False,
        help_text=_("Optional, leave empty for random password"),
    )
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput, required=False,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        """ checks that the email is unique """
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        """ check that the password was correctly repeated """

        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email[:30]
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User


class UserAdmin(DjangoUserAdmin):
    """ Configuration for the User admin page"""
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
