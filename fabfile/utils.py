from fabric.api import env, run, task, get, local, put
from fabric.context_managers import settings
from os.path import splitext, basename, dirname

from db import dump_db


@task
def backup_db():
    """ Backups database. """
    dump_name = dump_db(env.config.DB.name, env.config.DB.user,
                        env.config.DB.password)
    env.config.save()

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

    # unzip dump
    local('unzip -j "%s" -d %s' % (dump_name_zip, env.host))

    # database engine
    engine = env.config.local_DB.engine
    env.config.save()

    # import considering database engine
    if engine == 'mysql':
        local('echo "create database if not exists %s" | mysql -u root -p%s' %
              (env.config.local_DB.name, env.config.local_DB.password))
        local('mysql -u root -p%s %s < "%s"' % (env.config.local_DB.password,
                                                env.config.local_DB.name,
                                                dump_name))
        env.config.save()

    else:
        print 'Database engine not supported.'

    return dump_name_zip


@task
def export_db():
    """ Exports a database backup generated through `import_db()`. """
    dump_name_zip = import_db()
    dump_name = splitext(dump_name_zip)[0]  # name without zip extension

    # env.host replaced with staging host
    with settings(host_string=env.config.staging_DB.host):
        # upload the zipped file
        remote_path = put(dump_name_zip)[0]  # put returns a list

        # unzip dump
        run('unzip -j "%s" -d %s' % (basename(dump_name_zip), env.host))

        run('echo "create database if not exists %s" | mysql -u root -p%s' %
            (env.config.staging_DB.name, env.config.staging_DB.password))
        run('mysql -u root -p%s %s < "%s/%s"' %
            (env.config.staging_DB.password, env.config.staging_DB.name,
             env.host, basename(dump_name)))
        env.config.save()

        # cleanup files
        run('rm -f "%s"' % remote_path)  # zip file
        run('rm -f "%s/%s/%s"' % (dirname(remote_path), env.host,
                                  basename(dump_name)))  # raw file


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_checkout(branch):
    """ Utility method to change branches. """
    cmd = 'git checkout %s' % branch
    run(cmd)
