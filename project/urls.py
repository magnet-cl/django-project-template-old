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
