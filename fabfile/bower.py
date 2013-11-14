from fabric.api import task, env, run, cd
from fabric.colors import green


@task
def install():
    """ Installs bower. """
    print(green('Installing bower dependencies'))
    run('sudo npm install -g bower')
    update()


@task
def update():
    """ updates bower dependencies """
    print(green('Updating bower dependencies'))

    with cd(env.server_root_dir):
        with cd('base/static/'):
            run('bower install')
