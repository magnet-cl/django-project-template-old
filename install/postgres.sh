#!/bin/bash
yes | sudo apt-get install postgresql

echo "Would you like to set a password for your postgres user? [N/y]"
read SET_POSTGRES_PASSWORD
if [[ "$SET_POSTGRES_PASSWORD" == "y" ]]
then
    sudo -u postgres createuser --superuser $USER
    echo "\password $USER" | sudo -u postgres psql
    createdb $USER
fi
