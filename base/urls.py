""" this document defines the base app urls """
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^login/$','base.views.login', name='login'),
                       (r'^password_change/$', 'base.views.password_change'),
                       (r'^logout/$', 'base.views.logout'),
                       (r'^register/$', 'base.views.user_new'),

                       (r'^password_email_sent/$',
                        'base.views.password_reset_email_sent'),

                       (r'^password_reset/$', 'base.views.password_reset'),

                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-'
                           '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'base.views.password_reset_confirm',
                           name='password_reset_confirm'),

                       url(r'^verify/(?P<uidb36>[0-9A-Za-z]{1,13})-'
                           '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'base.views.user_new_confirm',
                           name='user_new_confirm'),

                       url(r'^reset/done/$',
                           'base.views.password_reset_complete', name='password_reset_complete'),
                       )
