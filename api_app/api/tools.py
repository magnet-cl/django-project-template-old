""" This document defines the tastytools tools for the API """
from api_app.api.resources import api
from tastytools.test.resources import ResourceTestData

class UserTestData(ResourceTestData):
    """ Test Data for the user resource """
    resource = "user"

api.register_testdata(UserTestData)
