""" decorators for the api """

# tastypie
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.bundle import Bundle

# standard library
import json


def api_method(single=False, expected_methods=['get'],
               returns_extra_data=False):
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
                if returns_extra_data:
                    objt = result[0]
                else:
                    objt = result
                bundle = resource.build_bundle(obj=objt, request=request)
                to_be_serialized = resource.full_dehydrate(bundle)
                if returns_extra_data:
                    to_be_serialized.data.update(result[1])
            else:  # if we are expecting an array of objects
                # we need to paginante
                paginator = resource._meta.paginator_class(
                    request.GET,
                    result,
                    resource_uri=resource.get_resource_uri(),
                    limit=resource._meta.limit,
                    max_limit=resource._meta.max_limit,
                    collection_name=resource._meta.collection_name)

                to_be_serialized = paginator.page()

                bundles = [resource.build_bundle(obj=obj, request=request)
                           for obj in to_be_serialized['objects']]

                to_be_serialized['objects'] = [resource.full_dehydrate(bnd)
                                               for bnd in bundles]

                resource.log_throttled_access(request)
            return resource.create_response(request, to_be_serialized)
        return wrapper
    return decorator


def required_fields(required_fields=[]):
    """ This decorator is to by applied only to the obj_create method of
    a ModelResource in your API

    If a required field is not present it generates an ImmediateHttpResponse
    in json with a reason explaining the problem

    """
    def decorator(func):
        """ The decorator applied to the obj_create method"""
        def wrapper(resource, bundle=None, **kwargs):
            """ wraps the decorated method and verifies a list of required
            fields when a new object is being created.

            """
            if not isinstance(bundle, Bundle):
                request = bundle
                data = resource.deserialize(
                    request, request.body,
                    format=request.META.get('CONTENT_TYPE', 'application/json')
                )
                bundle = resource.build_bundle(request=request, data=data)
            else:
                request = None

            for required_field in required_fields:
                if required_field not in bundle.data:
                    response = HttpBadRequest(
                        json.dumps("missing %s field" % required_field),
                        content_type=bundle.request.META['CONTENT_TYPE'])
                    raise ImmediateHttpResponse(response=response)
            return func(resource, bundle=bundle, **kwargs)
        return wrapper
    return decorator
