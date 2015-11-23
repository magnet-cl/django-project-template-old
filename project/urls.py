""" this document defines the project urls """

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('users.urls')),
    url(r'^$', 'base.views.index', name='home'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# custom error pages
handler404 = 'base.views.page_not_found_view'

handler500 = 'base.views.error_view'

handler403 = 'base.views.permission_denied_view'

handler400 = 'base.views.bad_request_view'
