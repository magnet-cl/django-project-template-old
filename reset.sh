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
    engine=`python -c"from project.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['ENGINE']"`
    debug=`python -c"from project.local_settings import LOCAL_DEBUG; print LOCAL_DEBUG"`
    dbname=`python -c"from project.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['NAME']"`
    south_installed=`python -c"from project.settings import INSTALLED_APPS; print 'south' in INSTALLED_APPS"`

    if [ $debug = "True" ] ; then
    echo "----------------------drop-database------------------------------"
        if [ $engine == "django.db.backends.sqlite3" ]; then
            if [ -f $dbname ] ; then
                echo "SQLITE: deleting $dbname"
                rm $dbname
            fi
        else
            dbuser=`python -c"from project.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['USER']"`
            dbpass=`python -c"from project.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['PASSWORD']"`
            if [ $engine == "django.db.backends.mysql" ]; then
                echo "drop database $dbname" | mysql --user=$dbuser --password=$dbpass
                echo "create database $dbname" | mysql --user=$dbuser --password=$dbpass
            else
                dropdb $dbname
                createdb $dbname
            fi
        fi
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

