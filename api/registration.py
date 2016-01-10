""" this document registers the resources into the API """

# resources
from users.resources import UserResource

# tastypie
from tastypie.api import Api

# api
from api.serializers import Serializer


api = Api(api_name='v1', serializer_class=Serializer)

api.register(UserResource())
