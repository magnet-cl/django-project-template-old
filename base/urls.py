""" this document defines the base app urls """
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       (r'^login/$', 'base.views.login'),
                       (r'^password_change/$', 'base.views.password_change'),
                       (r'^logout/$', 'base.views.logout'),
                       (r'^password_reset/$', 'base.views.password_reset'),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-'
                           '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'base.views.password_reset_confirm',
                           name='password_reset_confirm'),
                       url(r'^reset/done/$',
                           'base.views.password_reset_complete', name='password_reset_complete'),
                       )
