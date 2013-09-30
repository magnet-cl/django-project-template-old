#!/bin/bash

RUNSERVER=false
HEROKU=false
while getopts “sh” OPTION
do
    case $OPTION in
        s)
             echo "Start Server"
             RUNSERVER=true
             ;;
        h)
             echo "heroku restart"
             RUNSERVER=false
             HEROKU=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if  $HEROKU ; then
    heroku pg:reset DATABASE
    heroku run python manage.py syncdb
else
    debug=`python -c"from config.local_settings import LOCAL_DEBUG; print LOCAL_DEBUG"`
    south_installed=`python -c"from config.settings import INSTALLED_APPS; print 'south' in INSTALLED_APPS"`

    if [ $debug = "True" ] ; then
    echo "----------------------drop-database------------------------------"
        python manage.py dropdb
        echo "no" | python manage.py syncdb
        if [ $south_installed = "True" ] ; then
            python manage.py migrate --no-initial-data
            python manage.py migrate
        fi
    fi

    if  $RUNSERVER ; then
        python manage.py runserver
    fi
fi

