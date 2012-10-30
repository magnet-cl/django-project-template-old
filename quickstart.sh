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
    ./install/install-prerequisites
    virtualenv .env --distribute
    .env/bin/pip install --requirement install/requirements.pip
    source .env/bin/activate
    if [ -f ./config/local_settings.py ] ; then
        cp config/local_settings.py.default config/local_settings.py
    fi
fi
