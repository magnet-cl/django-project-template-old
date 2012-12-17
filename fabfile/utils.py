from fabric.api import env, run, task, get

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


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_checkout(branch):
    """ Utility method to change branches. """
    cmd = 'git checkout %s' % branch
    run(cmd)
