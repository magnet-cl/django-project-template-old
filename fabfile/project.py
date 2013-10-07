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
from utils import backup_db, git_clone, git_checkout


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
    """ Updates server repository and restarts gunicorn and nginx """
    update()
    restart()


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
    branch = prompt('Type in the branch to confirm: ')
    if host == env.host and branch == env.branch:
        # backup database before resetting
        backup_db()
        with cd(env.server_root_dir):
            with prefix('. .env/bin/activate'):
                run('./reset.sh')
    else:
        print('Invalid host or branch.')


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

    # install necessary dependencies to handle the project
    install_project_handling_dependencies()

    # clone repository
    git_clone(env.server_git_url, env.server_root_dir)

    # checkout branch
    with cd(env.server_root_dir):
        git_checkout(env.branch)

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


@task
def install_project_handling_dependencies():
    # install zip dependencies
    deb_handler.install('zip')
    deb_handler.install('unzip')
