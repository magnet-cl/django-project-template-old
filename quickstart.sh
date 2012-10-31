#!/bin/bash

INSTALL_APTITUDE=true
INSTALL_PIP=true
INSTALL_HEROKU=false
while getopts “ahp” OPTION
do
    case $OPTION in
        a)
             echo "only install aptitude"
             INSTALL_APTITUDE=true
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             ;;
        p)
             echo "only pip install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=true
             INSTALL_HEROKU=false
             ;;
        h)
             echo "only heroku install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if  $INSTALL_APTITUDE ; then
    # sudo install virtual env and other things with aptitude
    ./install/install-prerequisites

    # set a new virtual environment
    virtualenv .env --distribute
fi
if  $INSTALL_PIP ; then
    # activate the environment
    source .env/bin/activate

    # update easy_install (used by pip)
    easy_install -U distribute

    # install pip requiredments in the virtual environment
    .env/bin/pip install --requirement install/requirements.pip
fi
if  $INSTALL_HEROKU ; then
    # activate the environment
    source .env/bin/activate

    wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login
    pip install Django psycopg2 dj-database-url
    pip freeze > requirements.txt

    echo "Would you like to create a new heroku repo? [N/y]"
    read CREATE_REPO

    if [[ "$CREATE_REPO" == "y" ]]
    then
        heroku create
        echo "You should now commit the requirements.txt file."
        echo "Then deploy to heroku: git push heroku master"
    fi
fi

# create the local_settings file if it does not exist
if [ ! -f ./config/local_settings.py ] ; then
    cp config/local_settings.py.default config/local_settings.py
    EXP="s/django-db/${PWD##*/}/g"
    echo $i|sed -i $EXP config/local_settings.py
fi
