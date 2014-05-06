#!/bin/bash

INSTALL_APTITUDE=true
INSTALL_PIP=true
INSTALL_HEROKU=false
INSTALL_BOWER=true
INSTALL_NPM=true
while getopts “nahpb” OPTION
do
    case $OPTION in
        a)
             echo "only install aptitude"
             INSTALL_APTITUDE=true
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             ;;
        p)
             echo "only pip install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=true
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             ;;
        h)
             echo "only heroku install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=true
             INSTALL_BOWER=false
             INSTALL_NPM=false
             ;;
        b)
             echo "only bower install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=true
             INSTALL_NPM=false
             ;;
        n)
             echo "only node install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if  $INSTALL_APTITUDE ; then
    echo "Installing aptitude dependencies"

    # Install base packages
    yes | sudo apt-get install python-pip python-virtualenv python-dev 
    
    # Install image libs
    yes | sudo apt-get install libjpeg-dev zlib1g-dev zlib1g-dev

    echo "Are you going to use postgre for your database? [Y/n]"
    read INSTALL_POSTGRE

    if [[ "$INSTALL_POSTGRE" == "Y" ||  "$INSTALL_POSTGRE" == "y" ||  "$INSTALL_POSTGRE" == "" ]]
    then
        INSTALL_POSTGRE=true
        ./install/postgres.sh
    else
        echo "Are you going to use mysql for your database? [N/y]"
        read INSTALL_MYSQL

        if [[ "$INSTALL_MYSQL" == "y" ]]
        then
            # Install mysql related packages
            yes | sudo apt-get install libmysqlclient-dev python-mysqldb
        fi
    fi


    # set a new virtual environment
    virtualenv .env
fi
if  $INSTALL_PIP ; then
    # activate the environment
    source .env/bin/activate

    # install setuptools
    pip install --upgrade setuptools

    # install pip requiredments in the virtual environment
    .env/bin/pip install --download-cache=~/.pip-cache --requirement install/requirements.pip

    if [[ "$INSTALL_MYSQL" == "y" ]] ; then 
        pip install mysql-python
    fi

    if [[ "$INSTALL_POSTGRE" ]]
    then
        pip install psycopg2
    fi

fi

# update pip database requirements
source .env/bin/activate
if [[ "$INSTALL_MYSQL" == "y" ]]
then
    pip install MySQL-python
elif [[ "$INSTALL_POSTGRE" == "y" ]]
then
    pip install psycopg2
fi

# HEROKU 
if  $INSTALL_HEROKU ; then
    # activate the environment
    source .env/bin/activate

    wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login
    pip install psycopg2 dj-database-url
    pip freeze > requirements.txt
    pip uninstall psycopg2 dj-database-url

    echo "web: python manage.py runserver 0.0.0.0:$PORT --noreload" > Procfile

    echo "Would you like to create a new heroku repo? [N/y]"
    read CREATE_REPO

    if [[ "$CREATE_REPO" == "y" ]]
    then
        heroku create
    fi

    echo "You should now commit the requirements.txt file."
    echo "Then deploy to heroku: git push heroku master"
fi

# create the local_settings file if it does not exist
if [ ! -f ./config/local_settings.py ] ; then
    cp config/local_settings.py.default config/local_settings.py

    if [ INSTALL_POSTGRE ] ; then 
        EXP="s/database-name/${PWD##*/}/g"
        echo $i|sed -i $EXP config/local_settings.py
        
        echo "remember to set in config/local_setings.py your database"
        echo "settings"
    else
        EXP="s/postgresql_psycopg2/sqlite3/g"
        echo $i|sed -i $EXP config/local_settings.py

        EXP="s/database-name/\/tmp/${PWD##*/}.sql/g"
        echo $i|sed -i $EXP config/local_settings.py
    fi
fi

if  $INSTALL_BOWER ; then
    # bower.json modification
    EXP="s/NAME/${PWD##*/}/g"
    echo $i|sed -i $EXP bower.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    echo $i|sed -i $EXP bower.json

    ./node_modules/bower/bin/bower install
fi

if  $INSTALL_NPM ; then
    npm install
fi
