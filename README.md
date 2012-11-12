# django-project-template

A template for a Django project.

## Fabric tasks

In order to use fabric to deploy a gunicorn+nginx configuration you must set the following variables at `fabfile/config.py`:
* `env.server_root_dir`: Remote path of deployment.
* `env.server_git_url`: Your git repository.
* `env.server_domain`: Server domain of target server. (optional)
* `env.hosts`: Default host used by fabric. (optional)

and add a private ssh key file (id_rsa) to `fabfile/templates` named `ssh_key`. This file will be put in the remote server as the default ssh key for the remote user.

To get a list of the available tasks run: `fab -l`. 

Make sure to run the following task before any other task in any of the these formats:
* `fab config.set_host`: Uses the host specified in `env.hosts` and `magnet` as user.
* `fab config.set_host:examplehost`: Manually specify host.
* `fab config.set_host:examplehost,user`: Manually specify host and user.