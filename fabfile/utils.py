from fabric.api import env, run, task, get, local
from os.path import splitext

from db import dump_db


@task
def backup_db():
    """ Backups database. """
    dump_name = dump_db(env.config.DB.name, env.config.DB.user,
                        env.config.DB.password)
    env.config.save()

    return dump_name


@task
def download_db():
    """ Generates a database backup through `backup_db()` and downloads it. """
    return get('%s.zip' % backup_db())


@task
def import_db():
    """ Imports a zipped database backup generated through `download_db()`. """
    dump_name_zip = download_db()[0]  # download_db returns a list
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

    elif engine == 'postgis':  # TODO
        pass

    else:
        print 'Database engine not supported.'


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_checkout(branch):
    """ Utility method to change branches. """
    cmd = 'git checkout %s' % branch
    run(cmd)
