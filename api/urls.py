""" this document defines the project urls """

# django
from django.conf.urls import patterns, include, url

# resources
from campaigns.resources import CampaignResource
from clients.resources import ClientResource
from locations.resources import CommuneResource
from locations.resources import LocationResource
from locations.resources import RegionResource
from users.resources import UserResource

# tastypie
from tastypie.api import Api

# api
from api.serializers import Serializer


api = Api(api_name='v1', serializer_class=Serializer)

api.register(CampaignResource())
api.register(ClientResource())
api.register(CommuneResource())
api.register(LocationResource())
api.register(RegionResource())
api.register(UserResource())

urlpatterns = patterns(
    '',
    url(
        r'^v1/sync/$',
        'api.views.sync',
        name='api_sync'
    ),
    url(r'doc/', include('tastypie_swagger.urls',
                         namespace='tastypie_swagger')),
    (r'', include(api.urls)),
)
