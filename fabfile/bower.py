from fabric.api import task, env, run, cd


@task
def install():
    """ Installs bower. """
    run('sudo npm install -g bower')
    update()


@task
def update():
    """ updates bower dependencies """
    with cd(env.server_root_dir):
        with cd('base/static/'):
            run('bower install')
