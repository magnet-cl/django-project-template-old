""" this document defines the base app urls """
from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^login/$', 'base.views.login'),
)
