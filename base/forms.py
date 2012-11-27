from base.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader
from django.utils.http import int_to_base36
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
            return super(AuthenticationForm, self).clean()
        self.check_for_test_cookie()
        return self.cleaned_data


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
        widget=forms.PasswordInput,
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

    def save(self, verify_email_address=False, domain_override=None,
             subject_template_name='emails/user_new_subject.txt',
             email_template_name='emails/user_new.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, commit=True):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = user.email[:30]
        user.active = not verify_email_address

        if commit:
            user.save()

        if verify_email_address:
            from django.core.mail import send_mail

            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain

            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])

        return user



class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User


