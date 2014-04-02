""" Decorators for the campaigns view """


# django
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

# standard library
import json


def json_view(view):
    def wrap(req, *args, **kwargs):
        response = view(req, *args, **kwargs)
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                            content_type="application/json")
    return wrap
