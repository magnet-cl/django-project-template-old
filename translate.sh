#!/bin/bash

function print_green(){
    echo -e "\e[32m$1\e[39m"
}

function print_blue(){
    echo -e "\e[34m$1\e[39m"
}

function translate {
    if $COMPILE ; then
        django-admin.py compilemessages
    else
        django-admin.py makemessages -l es -e jade,html,txt,py
        django-admin.py makemessages -d djangojs -l es -i "base/static/bower_components" -i "node_modules" -e jade,js
    fi
}

COMPILE=false

while getopts “c” OPTION
do
    case $OPTION in
        c)
            print_blue "Compiling"
            COMPILE=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if [ $1 ] && [ $1 != '-c' ] ; then 
    print_blue "Translate only on app $1"
    cd $1
    translate
    cd ..
elif [ $2 ] && [ $2 != '-c' ] ; then 
    print_blue "Translate only on app $2"
    cd $2
    translate
    cd ..
else
    mkdir -p locale
    print_blue "Translate all apps"
    translate
fi
