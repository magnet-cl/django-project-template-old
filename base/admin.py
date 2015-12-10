""" Admin base configuration """

# django
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

# forms
from users.forms import AdminAuthenticationForm
from users.forms import CaptchaAuthenticationForm


# standard library
import csv


class AdminSite(admin.sites.AdminSite):
    login_form = AdminAuthenticationForm

    # Text to put at the end of each page's <title>.
    site_title = _('My site admin')

    # Text to put in each page's <h1>.
    site_header = _('My administration')

    # Text to put at the top of the admin index page.
    index_title = _('Site administration')

    @never_cache
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        from django.contrib.auth.views import login

        def captched_form(req=None, data=None):
            return CaptchaAuthenticationForm(
                req, data, initial={'captcha': request.META['REMOTE_ADDR']})

        # If the form has been submitted...
        template_name = "accounts/login.jade"

        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
        }
        context.update(extra_context or {})

        login_form = AdminAuthenticationForm

        if request.method == "POST":
            login_try_count = request.session.get('login_try_count', 0)
            request.session['login_try_count'] = login_try_count + 1

            if login_try_count >= 2:
                login_form = captched_form

        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or login_form,
            'template_name': self.login_template or template_name,
        }
        return login(request, **defaults)

admin.site = AdminSite()


def download_report(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)

    queryset = queryset.select_related()
    data = queryset.values()
    writer.writerow(data[0].keys())

    for datum in data:
        writer.writerow([unicode(s).encode("utf-8") for s in datum.values()])

    return response

download_report.short_description = _("Download Data")
