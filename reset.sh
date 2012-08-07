#!/bin/bash

engine=`python -c"from core.local_settings import DATABASES; print DATABASES['default']['ENGINE']"`
debug=`python -c"from core.local_settings import DEBUG; print DEBUG"`
dbname=`python -c"from core.local_settings import DATABASES; print DATABASES['default']['NAME']"`

if [ $debug = "True" ] ; then
echo "----------------------drop-database------------------------------"
    if [ $engine == "django.db.backends.mysql" ]; then
        dbuser=`python -c"from core.local_settings import DATABASES; print DATABASES['default']['USER']"`
        dbpass=`python -c"from core.local_settings import DATABASES; print DATABASES['default']['PASSWORD']"`
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
