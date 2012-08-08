""" this document defines the project urls """
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/v1/', include('api_app.urls')),
     url(r'^admin/', include(admin.site.urls)),
)
