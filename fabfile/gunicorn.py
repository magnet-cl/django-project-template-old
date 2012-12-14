from fabric.api import task, env, prefix, run, cd
from fabric.contrib.files import upload_template
from re import search

from service import add_upstart_task
from service import gunicorn_handler


@task
def install():
    """ Installs gunicorn. """
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('pip install gunicorn')


@task
def start():
    """ Starts the gunicorn service. """
    gunicorn_handler('start')


@task
def stop():
    """ Stops the gunicorn service. """
    if search('running', gunicorn_handler('status')):
        gunicorn_handler('stop')


@task
def restart():
    """ Restarts the gunicorn service. """
    gunicorn_handler('restart')


def add_gunicorn_script():
    """ Deploys a script to run django. """
    filename = '%s/fabfile/templates/gunicorn.sh'
    filename %= env.local_root_dir
    destination = env.server_root_dir
    context = {
        'user': env.user,
        'server_root_dir': env.server_root_dir,
        'django_port': env.django_port
    }
    upload_template(filename, destination, context=context, mode=0776)


@task
def add_gunicorn_service():
    """ Deploys a gunicorn configuration file. """

    # deploys the gunicorn script first
    add_gunicorn_script()

    filename = '%s/fabfile/templates/django.conf'
    filename %= env.local_root_dir
    gunicorn_script = '%s/gunicorn.sh'
    gunicorn_script %= env.server_root_dir
    context = {
        'gunicorn_script': gunicorn_script
    }

    add_upstart_task(filename, context)
