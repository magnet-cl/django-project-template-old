from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _
from django import forms


class AuthenticationForm(auth_forms.AuthenticationForm):
    """ Custom class for authenticating users. Takes the basic
    AuthenticationForm and adds email as an alternative for login
    """
    email = forms.EmailField(label=_("Email"))
    username = forms.CharField(label=_("Username"), max_length=30,
                               required=False)
    error_messages = auth_forms.AuthenticationForm.error_messages
    error_messages['invalid_email'] = _("Invalid email or password")

    def clean(self):
        """
        validates the email and password.
        It also validates the username and password using the django
        AuthenticationForm clean method
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_email'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        else:
            # check by username and password
            print "holi"
            return super(AuthenticationForm, self).clean()
        self.check_for_test_cookie()
        return self.cleaned_data
