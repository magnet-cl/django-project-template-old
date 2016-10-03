# django-project-template

A template for a Django project. It's simply project that was created with
Django 1.8.4 project with a lot of tweaks, usually things that we, at
Magnet.cl do in all projects.

## Requirements
* Python 2.7: This project was tested using python 2.7
* Node: This project uses node for bower, less and jade.

## Get the code
Create a new repository in github for your django project.
Clone your repository into your computer.
Add the django-project-template github repo as a remote repository:
* `git remote add template
  git@github.com:magnet-cl/django-project-template.git`
Pull the code from the project template
* `git pull template master` (there may be conflicts with your README.md file,
  fix them and continue)
Push to your own repo
* `git push origin master`
Now you have your own django project in your repository


## Quickstart

After you obtain the code, run the quick start script. It should install
all the dependencies you need to start the project. Then you need to Configure
your database settings in the project/local_settings.py file.

* `./quickstart.sh`

You can reset the database (drop if created, create, sync and load fixtures)
with:

* `./reset.sh`

## Basic Sturcture

### Settings: 

* Settings file is located on project/settings/__init__.py
    * Settings to modify:
        * RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY to set keys for the
        Captcha validator
        * ALLOWED_HOSTS: Set domains for Debug=False
        * SECRET_KEY: Changed automatically by quickstart.sh
* Local settings is located in project/settings/local_settings.py (this file
is not versioned)
    * Settings to modify:
         * Database configuration
         * Sendgrid configuration
         * Amazon configuration 
* A versioned copy of local settings is located on
project/settings/local_settings.default

### Base: 
Base is the first application of this project. It's function is to provide
the base for all other apps in your project. This is the place where you put
abstract model classes that are used throughout your project. 

* Custom models:
    * BaseModel: An abstract django model that all your models should inherit
      from. Contains the following methods
       * `update(self, *kwargs)`: updates in the database the fields you
         pass in the keyword arguments
       * `to_dict(self, fields=None, exclude=None)`: using the calling django 
         object, this method returns a dict with the model attributes. If the
         fields parameter is passed, only the specified attributes are
         included in the dict. By the contrary, if the exclude parameter is
         passed, then the excluded attributes will not be return in the dict.

* Admin: A basic configuration for the admin
* Json encoder: ModelEncoder
* Class base views in base/views.py
* BaseManager: Override the default manager
    * to_json
    * find_duplicates(fields): Find duplicates for the given fields
* Forms: BaseModelForm
    * adds css clases depending on the field class
    * Inherits BetterModelForms
* Mockups:
    * Create instances of models using the mockups (You have to define the
    method to create a mockup)
* Tests:
    * Use mockups to create objects to tests
    * Urls tests to check of 200 on every page is included
    * Integrity tests are placed to check on_delete attribute of fields
* view_utils.py:
    * clean_query_string

### Users: 
    * User: Custom user model that inherits form
      django.contrib.auth.models.User. This enables easy customization like
      adding new fieds or new methods. 
       * Simple email system to send templated emails.
       * Custom Backend for email authentication instead of username
         authentication
    * Fixtures: Fixtures on migration 0002

### Regions: 

### node_modules: 

### bower:

### scripts: 

* translate.sh
* quickstart.sh
* reset.sh

## Features

### Bootstrap 3 integration
Since We have been using bootstrap 3 for all our projects, we made that all
templates in the project are written for bootstrap 3.  

Also, the project compiles the source code for bootstrap 3 from less. This is
done so a rapid customization can be made of your site's style. The source
code for less is in `base/static/css/bootstrap/`

### Bootstrap 3 admin
bootstrap-admin==0.3.0
Since We have been using bootstrap 3 for all our project, we made that all
templates in the project are written for bootstrap 3. 
* bootstrap admin
* captcha login
* bower integration

### Fabric
It includes basic fabric tasks. These tasks are described later.

## Fabric tasks

In order to use fabric to deploy a gunicorn+nginx configuration you must set
the following variables at `fabfile/config.py`:
* `env.server_root_dir`: Remote path of deployment.
* `env.server_git_url`: Your git repository.
* `env.server_domain`: Server domain of target server. (optional)
* `env.hosts`: Default host used by fabric. (optional)

and add a private ssh key file (id_rsa) to `fabfile/templates` named
`ssh_key`. This file will be put in the remote server as the default ssh key
for the remote user.

To get a list of the available tasks run: `fab -l`. 

Make sure to run the following task before any other task in any of the these
formats:
* `fab config.set`: Uses the host specified in `env.hosts` and `magnet`
  as user.
* `fab config.set:examplehost`: Manually specify host.
* `fab config.set:examplehost,user`: Manually specify host and user.
