# api
from api.urls import api

# decorators
from base.decorators import json_view

# django

# models
from clients.models import Client
from locations.models import Location
from campaigns.models import Campaign
from users.models import User

# resources
from users.resources import UserResource


@json_view
def sync2(request):
    campaigns = Campaign.objects.all()
    clients = Client.objects.all()
    locations = Location.objects.all()
    users = User.objects.all()

    data = {
        'clients': list(clients.values()),
        'campaigns': list(campaigns.values()),
        'users': list(users.values()),
        'locations': list(locations.values()),
        'shifts': [],
        'statuses': [],
    }
    return data


@json_view
def sync(request):
    res = UserResource()

    bundles = {
        'users': prepare_bundle(request, 'user'),
        'campaigns': prepare_bundle(request, 'campaign'),
        'locations': prepare_bundle(request, 'location'),
        'clients': prepare_bundle(request, 'client'),
        'shifts': [],
        'statuses': [],
    }

    return res.serialize(None, bundles, "application/json")


def prepare_bundle(request, resource_name):
    res = api.canonical_resource_for(resource_name)

    request_bundle = res.build_bundle(request=request)
    queryset = res.obj_get_list(request_bundle)

    bundles = []
    for obj in queryset:
        bundle = res.build_bundle(obj=obj, request=request)
        bundles.append(res.full_dehydrate(bundle, for_list=True))

    return bundles
