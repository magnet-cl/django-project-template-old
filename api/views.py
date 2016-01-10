# decorators
from base.decorators import json_view

# django
from django.http import HttpResponse


@json_view
def upgrade_required(request):
    return HttpResponse(status=426)
