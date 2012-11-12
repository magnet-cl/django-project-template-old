from fabric.api import cd, env, run, task
from fabric.colors import green, red
from fabric.context_managers import settings, hide
from fabric.utils import warn
from re import search

from db import dump_db


@task
def backup_db():
    """ Backups database. """
    dump_db(env.config.DB.name, env.config.DB.user, env.config.DB.password)
    env.config.save()


def git_clone(url):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s' % url
    run(cmd)
