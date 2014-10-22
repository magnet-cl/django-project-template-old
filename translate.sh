#!/bin/bash
green='\e[0;32m'
NC='\e[0m' # No Color

function makemessages {
    cd $1


    django-admin.py makemessages -l es -e jade,html,txt,py
    diff=$(git diff --numstat locale/es/LC_MESSAGES/django.po)
    lineCount=(${diff// / })
    if [ $lineCount == 1 ] ; then
        git checkout locale/es/LC_MESSAGES/django.po
    fi

    cd ..
}

function translate {
    echo -e "${green}translating $1${NC}"
    if $COMPILE ; then
        cd $1
        django-admin.py compilemessages
        cd ..
    else
        makemessages $1
    fi
}

COMPILE=false

while getopts “c” OPTION
do
    case $OPTION in
        c)
            COMPILE=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if [ $2 ] ; then 
    translate $2
else
    translate "users"
    translate "base"
    translate "project"
fi
