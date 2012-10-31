#!/bin/bash

RUNSERVER=false
while getopts “s” OPTION
do
    case $OPTION in
        s)
             echo "Start Server"
             RUNSERVER=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

engine=`python -c"from config.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['ENGINE']"`
debug=`python -c"from config.local_settings import LOCAL_DEBUG; print LOCAL_DEBUG"`
dbname=`python -c"from config.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['NAME']"`

if [ $debug = "True" ] ; then
echo "----------------------drop-database------------------------------"
    if [ $engine == "django.db.backends.mysql" ]; then
        dbuser=`python -c"from config.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['USER']"`
        dbpass=`python -c"from config.local_settings import LOCAL_DATABASES; print LOCAL_DATABASES['default']['PASSWORD']"`
        echo "drop database $dbname" | mysql --user=$dbuser --password=$dbpass
        echo "create database $dbname" | mysql --user=$dbuser --password=$dbpass
    else
        if [ -f $dbname ] ; then
            echo "SQLITE: deleting $dbname"
            rm $dbname
        fi
    fi
    echo "no" | python manage.py syncdb
    python manage.py migrate
fi

if  $RUNSERVER ; then
    python manage.py runserver
fi

