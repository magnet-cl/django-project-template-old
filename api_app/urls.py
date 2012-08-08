""" this document defines the api urls """

from django.conf.urls.defaults import patterns, include
from api_app.api.tools import api


urlpatterns = patterns('',
    (r'^doc/$', 'tastytools.views.doc', {'api_name': api.api_name}),
    (r'', include(api.urls)),
)
