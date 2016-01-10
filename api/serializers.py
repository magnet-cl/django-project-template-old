from tastypie.serializers import Serializer as TastypieSerializer

import json


class Serializer(TastypieSerializer):
    """
    Replace the base Serializer for one that returns an aswer to html and
    the variables in camel case
    """

    formats = ['json']
    content_types = {
        'json': 'application/json',
    }

    def to_html(self, data, options=None):
        """
        Overrride the to_html method to return json, since it's more helpful
        """
        return self.to_json(data, options)

    def to_json(self, data, options=None):
        """
        """
        data = self.to_simple(data, options)

        return json.dumps(data, sort_keys=True)

    def from_json(self, content):
        """
        """
        data = json.loads(content)

        return data
