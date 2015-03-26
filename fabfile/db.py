from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import local
from fabric.api import prefix
from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import red
from fabric.context_managers import settings

# standard library
from os.path import splitext
from os.path import dirname
from os import environ
from time import gmtime
from time import strftime
import sys


# add django settings module to the import search path
sys.path.append(dirname(dirname(__file__)))
environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


@task
def get_db_name():
    """ Returns the name of the default database """
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            return run('python manage.py printdatabasename')


@task
def migrate():
    """ Migrates database to the latest south migration """
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('python manage.py migrate --no-initial-data')


@task
def backup_db():
    """ Backups database (postgreSQL). """
    # get database name
    db_name = get_db_name()

    # dumps folder creation
    dumps_folder = 'db_dumps/{}'.format(env.branch)
    cmd = 'mkdir -p {}'.format(dumps_folder)
    run(cmd)
    # generate backup file name based on its branch and current time
    dump_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    dump_name = '{}/{}.sql.gz'.format(dumps_folder, dump_name)

    cmd = 'pg_dump {} | gzip > "{}"'.format(db_name, dump_name)
    run(cmd)

    return dump_name


@task
def download_db(compressed_file=None):
    """ Downloads the given compressed dump or generates it through
    `backup_db()` and downloads it. """

    if compressed_file is None:
        compressed_file = backup_db()

    # get returns a list, the first element is returned
    return get(compressed_file)[0]


@task
def import_db(compressed_file=None):
    """ Imports a compressed database backup into the local system.

    In order to use this task, your local database engine must be postgreSQL.

    """
    # local django settings
    from django.conf import settings as django_settings

    if compressed_file is None:
        compressed_file = download_db(compressed_file)

    # name without gzip extension
    dump_name = splitext(compressed_file)[0]

    # gunzip dump
    local('gunzip "{}"'.format(compressed_file))

    # get local database information
    local_engine = django_settings.DATABASES['default']['ENGINE']
    local_name = django_settings.DATABASES['default']['NAME']

    # check local database engine
    if local_engine != 'django.db.backends.postgresql_psycopg2':
        print(red('Please set your local database engine to postgreSQL.'))
        print(red('Aborting current task.'))
        return

    local('echo "drop database if exists {}" | psql'.format(local_name))
    local('echo "create database {}" | psql'.format(local_name))
    local('psql {} < "{}"'.format(local_name, dump_name))

    return compressed_file


@task
def export_db(compressed_file=None):
    """ Exports the given compressed database backup into a staging server.

    If no compressed_file is given, then it is generated through
    `download_db()`.

    """

    if compressed_file is None:
        compressed_file = download_db(compressed_file)

    # name without gzip extension
    dump_name = splitext(compressed_file)[0]

    # env.host replaced with staging host
    with settings(host_string=env.config.staging_DB.host):
        # get database name on staging
        db_name = get_db_name()

        # upload the compressed file
        compressed_file = put(compressed_file)[0]  # put returns a list
        dump_name = splitext(compressed_file)[0]  # name without gzip extension

        # gunzip dump
        run('gunzip "{}"'.format(compressed_file))

        run('echo "drop database if exists {}" | psql'.format(db_name))
        run('echo "create database {}" | psql'.format(db_name))
        run('psql {} < "{}"'.format(db_name, dump_name))

        # cleanup files
        run('rm -f "{}"'.format(dump_name))  # raw file
