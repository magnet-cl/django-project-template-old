"""
Abstract resources to be used instead of tastypie.resources.ModelResource
"""

# decorators
from api.decorators import api_method

# tastypie
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource

# other
from api.serializers import Serializer

# standard library
from base64 import urlsafe_b64encode
from os import urandom
from os.path import splitext
import logging

# Get an instance of a logger
logger = logging.getLogger('api')


class BaseModelResource(ModelResource):
    """ the base class of every Api Resource """
    class Meta:
        """ Metadata for the Api resource """
        always_return_data = True
        serializer = Serializer()

    def determine_format(self, request):
        """ override the determine_format method to return application/json
        if the format given is text/html

        """

        format = super(BaseModelResource, self).determine_format(request)
        if format == "text/html":
            return "application/json"
        return format

    def attach_upload(self, request, resource_name, pk, **kwargs):
        response = super(BaseModelResource, self).attach_upload(
            request, resource_name, pk, **kwargs)

        if type(response) == http.HttpResponse:
            return self.get_detail(request, id=pk)
        return response

    def full_dehydrate_list(self, objects, request=None):
        # Dehydrate the bundles in preparation for serialization.

        bundles = []
        for obj in objects:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        return bundles

    def json_serialize_list(self, objects, request=None):
        bundles = self.full_dehydrate_list(objects, request)
        return self.serialize(None, bundles, "application/json")

    def full_dehydrate_obj(self, obj, request=None):
        bundle = self.build_bundle(obj=obj, request=request)
        return self.full_dehydrate(bundle)

    def unauthorized_result(self, exception):
        response = http.HttpUnauthorized()
        response['WWW-Authenticate'] = 'Password required'
        raise ImmediateHttpResponse(response=response)


class MultipartResource(BaseModelResource):
    def deserialize(self, request, data, format=None):
        logger.debug('MultipartResource.deserialize')
        logger.debug(
            'MultipartResource.deserialize. Format: {}'.format(format))

        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        # TODO remove this when the following issue is fixed
        # https://github.com/concentricsky/django-tastypie-swagger/issues/76
        if format == 'text/plain':
            return request.GET

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)

            return data

        # TODO remove this try catch when the following issue is fixed
        # https://github.com/concentricsky/django-tastypie-swagger/issues/76
        try:
            return super(MultipartResource, self).deserialize(
                request, data, format)
        except Exception as e:
            if not request.META.get('CONTENT_TYPE'):
                return request.GET
            raise(e)

    @api_method(expected_methods=['post'], single=True)
    def update(self, request, **kwargs):
        bundle = self.build_bundle(request=request)

        obj = self.cached_obj_get(bundle=bundle,
                                  **self.remove_api_resource_names(kwargs))

        for file_name, _file in request.FILES.items():
            setattr(obj, file_name, _file)

        for attr, value in request.POST.items():
            setattr(obj, attr, value)

        obj.save()

        return obj

    def upload_tmp_file(self, request):
        """ Generic method to upload temporary files.

        Returns
            tmp_file: Temporary file name path
            None: If no FILES present on request

        """
        # check if FILES dict is empty
        if request.FILES:
            for file_name in request.FILES:
                raw_file = request.FILES[file_name]
                file_extension = splitext(str(raw_file))[1]
                # unique name for temporary file
                tmp_file = urlsafe_b64encode(urandom(30))[:30]
                # folder and extension
                tmp_file = '/tmp/{}{}'.format(tmp_file, file_extension)

                # saving by chunks into a temporary file
                with open(tmp_file, 'wb') as destination:
                    for chunk in raw_file:
                        destination.write(chunk)
                return tmp_file
