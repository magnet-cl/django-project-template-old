""" this document defines the users app urls """
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^login/$', 'users.views.login', name='login'),
    (r'^password_change/$', 'users.views.password_change'),
    (r'^logout/$', 'users.views.logout'),
    (r'^register/$', 'users.views.user_new'),

    (r'^password_email_sent/$',
     'users.views.password_reset_email_sent'),

    (r'^password_reset/$', 'users.views.password_reset'),

    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'users.views.password_reset_confirm',
        name='password_reset_confirm'),

    url(r'^verify/(?P<uidb36>[0-9A-Za-z]{1,13})-'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'users.views.user_new_confirm',
        name='user_new_confirm'),

    url(r'^reset/done/$',
        'users.views.password_reset_complete',
        name='password_reset_complete'),
)
