from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """ Prints the default database name """
        self.stdout.write(settings.DATABASES['default']['NAME'])
