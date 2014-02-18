from fabric.api import env, run, task, get, local, put
from fabric.context_managers import settings
from os.path import splitext
from time import gmtime, strftime


@task
def backup_db():
    """ Backups database (postgreSQL). """
    db_name = env.config.DB.name
    env.config.save()

    # generating dump file name
    dumps_folder = "db_dumps/%s" % env.branch
    cmd = "mkdir -p %s" % dumps_folder
    run(cmd)
    dump_name = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dump_name = "%s/%s.sql.gz" % (dumps_folder, dump_name)

    cmd = 'pg_dump %s | gzip > "%s"' % (db_name, dump_name)
    run(cmd)

    return dump_name


@task
def download_db(zip_file=None):
    """ Generates a database backup through `backup_db()` and downloads it. """

    if zip_file is None:
        zip_file = '%s.zip' % backup_db()

    return get(zip_file)


@task
def import_db(zip_file=None):
    """ Imports a zipped database backup generated through `download_db()`. """

    dump_name_zip = download_db(zip_file)[0]  # download_db returns a list
    dump_name = splitext(dump_name_zip)[0]  # name without zip extension

    # gunzip dump
    local('gunzip "%s"' % dump_name_zip)

    # database engine
    engine = env.config.local_DB.engine
    env.config.save()

    # import considering database engine
    if engine == 'psql':
        local('echo "drop database if exists %s" | psql' %
              env.config.local_DB.name)
        local('echo "create database %s" | psql' % env.config.local_DB.name)
        local('psql %s < "%s"' % (env.config.local_DB.name, dump_name))
        env.config.save()

    else:
        print 'Database engine not supported.'

    return dump_name_zip


@task
def export_db():
    """ Exports a database backup generated through `download_db()` into a
    staging server."""
    dump_name_zip = download_db()[0]  # download_db returns a list
    dump_name = splitext(dump_name_zip)[0]  # name without zip extension

    # env.host replaced with staging host
    with settings(host_string=env.config.staging_DB.host):
        # upload the zipped file
        dump_name_zip = put(dump_name_zip)[0]  # put returns a list
        dump_name = splitext(dump_name_zip)[0]  # name without zip extension

        # gunzip dump
        run('gunzip "%s"' % dump_name_zip)

        run('echo "drop database if exists %s" | psql' %
            env.config.staging_DB.name)
        run('echo "create database %s" | psql' % env.config.staging_DB.name)
        run('psql %s < "%s"' % (env.config.staging_DB.name, dump_name))
        env.config.save()

        # cleanup files
        run('rm -f "%s"' % dump_name)  # raw file


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_checkout(branch):
    """ Utility method to change branches. """
    cmd = 'git checkout %s' % branch
    run(cmd)
