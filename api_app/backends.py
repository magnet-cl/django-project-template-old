from api_app.models import User


class ApiBackend(object):
    """
    Authenticates against api_app.models.User
    """
    supports_inactive_user = True

    def authenticate(self, email=None, username=None, password=None, token=None):
        """ login using  the username validating with the password  or the
        token. If the token is used, then it's deleted

        """
        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(email=email)
        except User.DoesNotExist:
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
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
