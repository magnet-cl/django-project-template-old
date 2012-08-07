from api_app.models import ApiUser


class ApiBackend(object):
    """
    Authenticates against api_app.models.ApiUser
    """
    supports_inactive_user = True

    def authenticate(self, email=None, password=None, token=None):
        """ login using  the email validating with the password  or the
        token. If the token is used, then it's deleted

        """
        try:
            user = ApiUser.objects.get(email=email)
        except ApiUser.DoesNotExist:
            return None
        if password is not None:
            if user.check_password(password):
                return user
        if token:
            if user.token == token and len(token) == 30:
                user.token = ""
                user.is_active=True
                user.save()
                return user
        return None


    def get_user(self, user_id):
        """ returns the user using the id """
        try:
            return ApiUser.objects.get(pk=user_id)
        except ApiUser.DoesNotExist:
            return None
