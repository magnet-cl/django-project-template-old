""" decorators for the api """

from django.core.paginator import Paginator, InvalidPage
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
import json

def api_method(single=False, expected_methods=['get']):
    """
    api_method is a decorator with parameters for a custom api endpint, dealing
    with the common tasks that does not concern the method itself, like
    checking if the request method is allowed or packing the response in an
    api friendly way

    input
    * sigle: if the response is meant to return a single object or an array

    output: returns a resource response, with the request and the result
    of the decorated method

    """
    def decorator(func):
        """ The decorator applied to the endpoint """
        def wrapper(resource, request, ** kwargs):
            """ wraps the method with common api response's routines, like
            checking if it's authenticated or packing the response in an api
            friendly way

            """
            # ckech if everything is ok, before proceding
            resource.method_check(request, allowed=expected_methods)
            resource.is_authenticated(request)
            resource.throttle_check(request)

            # call the decorated method
            result = func(resource, request, **kwargs)

            # if a single response is expected
            if single:
                bundle = resource.build_bundle(obj=result, request=request)
                bundle = resource.full_dehydrate(bundle)
                object_list = bundle
            else: #  if we are expecting an array of objects
                #we need to paginante
                paginator = Paginator(result, 20)

                try:
                    page = paginator.page(int(request.GET.get('page', 1)))
                except InvalidPage:
                    response = HttpNotFound(
                            json.dumps("Sorry, no results on that page."),
                            content_type=request.META['CONTENT_TYPE'])
                    raise ImmediateHttpResponse(response=response)

                objects = []

                for obj in page.object_list:
                    bundle = resource.build_bundle(obj=obj, request=request)
                    bundle = resource.full_dehydrate(bundle)
                    objects.append(bundle)

                object_list = {
                    'objects': objects,
                }

                resource.log_throttled_access(request)
            return resource.create_response(request, object_list)
        return wrapper
    return decorator
