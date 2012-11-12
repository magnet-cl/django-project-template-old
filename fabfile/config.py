from artichoke import Config as ArtichokeConfig
from fabric.api import env, task
from os import path

# local and remote paths
env.local_root_dir = path.join(path.dirname(__file__), "..")
env.server_root_dir = 'example/path'

# server domain used by nginx
env.server_domain = 'example.com'

# git repositories
env.server_git_url = 'example/url.git'

class Config(ArtichokeConfig):
    def __init__(self, env, config_file=None):
        super(Config, self).__init__(config_file)

        self.add_section('DB')

config_file = '%s/config.ini' % env.local_root_dir
env.config = Config(env, config_file)


@task
def set_host(host='cl', user='magnet'):
    """ Host and user setter with shortcuts. """
    # host
    if host == 'cl':
        env.hosts = ['example.com']
    else:
        # TODO Validate input
        env.hosts = [host]

    # user
    env.user = user
