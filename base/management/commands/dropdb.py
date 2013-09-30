# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.management.sql import sql_delete
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.exceptions import ImproperlyConfigured
from django.core.management.color import no_style

from optparse import make_option


class Command(BaseCommand):
    help = "Drops all tables for the given app name(s). (defaults to all)"
    output_transaction = True

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
                    default=DEFAULT_DB_ALIAS,
                    help='Nominates a database for drop. '
                    'Defaults to the "default" database.'),
    )

    def handle(self, *app_labels, **options):
        from django.db import models
        if not app_labels:
            app_list = models.get_apps()
        else:
            try:
                app_list = [models.get_app(app_lbl) for app_lbl in app_labels]
            except (ImproperlyConfigured, ImportError) as e:
                raise CommandError("%s. Are you sure your INSTALLED_APPS "
                                   "setting is correct?" % e)
        output = []
        for app in app_list:
            app_output = self.handle_app(app, **options)
            if app_output:
                output.append(app_output)
        return '\n'.join(output)

    def handle_app(self, app, **options):
        db = options.get('database')
        connection = connections[db]

        commands = sql_delete(app, no_style(), connection)

        for command in commands:
            cursor = connection.cursor()
            cursor.execute(command)
