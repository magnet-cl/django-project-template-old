from django.core.management.templates import TemplateCommand
from django.utils.crypto import get_random_string

import fileinput


class Command(TemplateCommand):
    help = ("Replaces the SECRET_KEY VALUE in config/settings.py with a new"
            "one.")

    def handle(self, *args, **options):
        # Create a random SECRET_KEY hash to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)

        for line in fileinput.input("config/settings.py", inplace=True):
            if line.startswith("SECRET_KEY = "):
                print "SECRET_KEY = '{}'".format(secret_key)
            else:
                print "%s" % line,
