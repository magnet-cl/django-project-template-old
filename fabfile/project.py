from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import prompt
from fabric.api import put
from fabric.api import run
from fabric.api import task

import gunicorn
import nginx
import deb_handler
from db import install_mysql
from utils import backup_db, git_clone


@task
def update():
    """ Updates server repository. """
    update_server()


def update_helper(root_dir):
    with cd(root_dir):
        run('git pull')


@task
def update_server():
    """ Updates server repository. """
    # backup database before updating
    backup_db()

    update_helper(env.server_root_dir)
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('pip install --requirement install/requirements.pip')
            run('yes yes | python manage.py collectstatic')


@task
def restart():
    """ Restarts gunicorn and nginx. """
    gunicorn.restart()
    nginx.restart()


@task
def update_restart():
    """ Restarts gunicorn and nginx. """
    restart()
    update()


@task
def stop():
    """ Stops gunicorn and nginx. """
    gunicorn.stop()
    nginx.stop()


@task
def start():
    """ Starts gunicorn and nginx. """
    gunicorn.start()
    nginx.start()


@task
def db_reset():
    """ Resets database. """
    print('Are you sure you want to reset the database?')
    host = prompt('Type in the host to confirm: ')
    if host == env.host:
        # backup database before resetting
        backup_db()
        with cd(env.server_root_dir):
            with prefix('. .env/bin/activate'):
                run('./reset.sh')
    else:
        print('Invalid host: %s != %s' % (host, env.host))


@task
def initial_deploy():
    """ Performs a complete deploy of the project. """

    # put ssh key
    ssh_key = '%s/fabfile/templates/ssh_key'
    ssh_key %= env.local_root_dir
    run('mkdir -p -m 0700 .ssh')
    put(ssh_key, '.ssh/id_rsa', mode=0600)

    # github host handshake
    run('ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts')

    # clone repository
    deb_handler.install('git')
    git_clone(env.server_git_url)

    # mysql installation
    install_mysql()

    # dependencies installation (quickstart)
    with cd(env.server_root_dir):
        run('./quickstart.sh')

    # gunicorn installation and configuration
    gunicorn.install()
    gunicorn.add_gunicorn_service()
    gunicorn.start()

    # nginx installation and configuration
    nginx.install()
    nginx.add_django_site()
    nginx.start()
