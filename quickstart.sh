#!/bin/bash

function print_green(){
    echo -e "\e[32m$1\e[39m"
}

INSTALL_APTITUDE=true
INSTALL_PIP=true
INSTALL_HEROKU=false
INSTALL_BOWER=true
INSTALL_NPM=true
TRANSLATE=true
while getopts “nahpb” OPTION
do
    case $OPTION in
        a)
             print_green "only install aptitude"
             INSTALL_APTITUDE=true
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        p)
             print_green "only pip install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=true
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        h)
             print_green "only heroku install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=true
             INSTALL_BOWER=false
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        b)
             print_green "only bower install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=true
             INSTALL_NPM=false
             TRANSLATE=false
             ;;
        n)
             print_green "only node install"
             INSTALL_APTITUDE=false
             INSTALL_PIP=false
             INSTALL_HEROKU=false
             INSTALL_BOWER=false
             INSTALL_NPM=true
             TRANSLATE=false
             ;;
        ?)
             print_green "fail"
             exit
             ;;
     esac
done

if  $INSTALL_APTITUDE ; then
    print_green "Installing aptitude dependencies"

    # Install base packages
    sudo apt-get -y install python-pip python-virtualenv python-dev build-essential

    print_green "Installing image libraries"
    # Install image libs
    sudo apt-get -y install libjpeg-dev zlib1g-dev zlib1g-dev

    print_green "Installing translation libraries"
    sudo apt-get -y install gettext

    print_green "Are you going to use postgre for your database? [Y/n]"
    read INSTALL_POSTGRE

    if [[ "$INSTALL_POSTGRE" == "Y" ||  "$INSTALL_POSTGRE" == "y" ||  "$INSTALL_POSTGRE" == "" ]]
    then
        INSTALL_POSTGRE=true
        ./install/postgres.sh
    else
        print_green "Are you going to use mysql for your database? [N/y]"
        read INSTALL_MYSQL

        if [[ "$INSTALL_MYSQL" == "y" ]]
        then
            # Install mysql related packages
            sudo apt-get -y install libmysqlclient-dev python-mysqldb
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

    # upgrade pip
    pip install --upgrade pip

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

    print_green "web: python manage.py runserver 0.0.0.0:$PORT --noreload" > Procfile

    print_green "Would you like to create a new heroku repo? [N/y]"
    read CREATE_REPO

    if [[ "$CREATE_REPO" == "y" ]]
    then
        heroku create
    fi

    print_green "You should now commit the requirements.txt file."
    print_green "Then deploy to heroku: git push heroku master"
fi

# create the local_settings file if it does not exist
if [ ! -f ./project/local_settings.py ] ; then
    cp project/local_settings.py.default project/local_settings.py

    if [ INSTALL_POSTGRE ] ; then 
        EXP="s/database-name/${PWD##*/}/g"
        print_green $i|sed -i $EXP project/local_settings.py
        
        print_green "remember to configure in project/local_setings.py your database"
    else
        EXP="s/postgresql_psycopg2/sqlite3/g"
        print_green $i|sed -i $EXP project/local_settings.py

        EXP="s/database-name/\/tmp/${PWD##*/}.sql/g"
        print_green $i|sed -i $EXP project/local_settings.py
    fi
fi

# Change the project/settings.py file it contains the CHANGE ME string
if grep -q "CHANGE ME" "project/settings.py"; then
    # change the SECRET_KEY value on project settings
    python manage.py generatesecretkey
fi


if  $INSTALL_NPM ; then
    # package.json modification
    EXP="s/NAME/${PWD##*/}/g"
    print_green $i|sed -i $EXP package.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    print_green $i|sed -i $EXP package.json

    npm install
fi

if  $INSTALL_BOWER ; then
    # bower.json modification
    EXP="s/NAME/${PWD##*/}/g"
    print_green $i|sed -i $EXP bower.json
    EXP="s/HOMEPAGE/https:\/\/bitbucket.org\/magnet-cl\/${PWD##*/}/g"
    print_green $i|sed -i $EXP bower.json

    ./node_modules/bower/bin/bower install
fi
 
if $TRANSLATE ; then 
    ./translate.sh -c
fi
