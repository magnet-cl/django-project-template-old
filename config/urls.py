""" this document defines the project urls """

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('base.urls')),
     (r'^$', 'base.views.index'),
)

if settings.DEBUG:
   urlpatterns += patterns('',
                           (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
                            'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))
