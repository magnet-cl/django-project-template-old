from fabric.api import env
from fabric.api import sudo
from fabric.contrib.files import upload_template


def handler(service, action):
    """ Handler method for service operations. """
    cmd = 'service %s %s' % (service, action)
    return sudo(cmd, pty=False)


def nginx_handler(action):
    """ Helper method for nginx service operations. """
    return handler('nginx', action)


def gunicorn_handler(action):
    """ Helper method for gunicorn instance service operations. """
    instance = 'django-{}-{}'.format(env.prefix, env.branch)
    return handler(instance, action)


def add_upstart_task(filename, context):
    """ Deploys an upstart configuration task file. """
    destination = '/etc/init/django-{}-{}.conf'.format(env.prefix, env.branch)
    upload_template(filename, destination, context=context, use_sudo=True)
