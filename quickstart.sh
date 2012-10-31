#!/bin/bash

ONLY_PIP_INSTALL=false
while getopts “p” OPTION
do
    case $OPTION in
        p)
             echo "only pip install"
             ONLY_PIP_INSTALL=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if  $ONLY_PIP_INSTALL ; then
    .env/bin/pip install --requirement install/requirements.pip
else
    # sudo install virtual env and other things with aptitude
    ./install/install-prerequisites

    # set a new virtual environment
    virtualenv .env --distribute

    # activate the environment
    source .env/bin/activate

    # update easy_install (used by pip)
    easy_install -U distribute

    # install pip requiredments in the virtual environment
    .env/bin/pip install --requirement install/requirements.pip

    # create the local_settings file if it does not exist
    if [ ! -f ./config/local_settings.py ] ; then
        cp config/local_settings.py.default config/local_settings.py
    fi
fi
