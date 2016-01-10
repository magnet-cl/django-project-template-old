from tastypie.authentication import SessionAuthentication


class MethodWardAuthentication(SessionAuthentication):
    """ Use when authentication requirement varies by the method being used."""

    def __init__(self, annonymus_allowed_methods=[], *args, **kwargs):
        """Constructor. Expects a list of HTTP methods which are allowed
        WITHOUT authentication, all other methods will require
        authentication"""

        self.annonymus_allowed_methods = [
            x.upper() for x in annonymus_allowed_methods]
        super(MethodWardAuthentication, self).__init__()

    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True

        if request.method in self.annonymus_allowed_methods:
            return True

        return super(MethodWardAuthentication, self).is_authenticated(
            request, **kwargs)

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns a combination of IP address and hostname
        if the user is not authenticated.
        """
        if request.user.is_authenticated():
            return super(MethodWardAuthentication, self).get_identifier(
                request)
        return "%s_%s" % (request.META.get('REMOTE_ADDR', 'noaddr'),
                          request.META.get('REMOTE_HOST', 'nohost'))
