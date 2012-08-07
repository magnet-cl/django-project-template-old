""" This file demonstrates writing tests using the unittest module. These will
pass when you run "manage.py test".

"""
from api_app.models import ApiUser
from api_app.api.tools import api
from mockups.contrib.auth import UserMockup
from tastytools.test.definitions import resources, fields


def resourceSetUp(self, *args, **kwargs):
    password = 'superpassword'
    user_mockup = UserMockup(ApiUser, password=password, generate_fk=True)
    user = user_mockup.create_one()

    self.assertTrue(self.client.login(
        email=user.email,
        password=password
        ),
        "Could not login as %s/%s" % (user.username, password)
    )

ResourceTests = resources.generate(api, setUp=resourceSetUp)
ResourceFieldTests = fields.generate(api, setUp=resourceSetUp)
