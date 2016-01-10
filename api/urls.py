""" this document defines the project urls """

# django
from django.conf.urls import include
from django.conf.urls import patterns
 from django.conf.urls import url

# api
from api.registration import api

urlpatterns = patterns(
    '',
    # url(
    #     r'doc/', include(
    #         'tastypie_swagger.urls',
    #         namespace='tastypie_swagger'),
    #     kwargs={
    #         "tastypie_api_module": "api.urls.api",
    #         "namespace": "tastypie_swagger"}
    # ),
    (r'', include(api.urls)),
)
