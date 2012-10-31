""" this document defines the project urls """
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     (r'^accounts/', include('base.urls')),
     (r'^$', 'base.views.index'),
)
