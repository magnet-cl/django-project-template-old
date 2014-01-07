BASE_FIXTURES_PATH="base/fixtures/initial_data.json"

python manage.py dumpdata auth.group > $BASE_FIXTURES_PATH --natural --indent=4
NUMOFLINES=$(wc -l < $BASE_FIXTURES_PATH)

if [ $NUMOFLINES -lt 3 ] ; then 
    rm $BASE_FIXTURES_PATH
fi
python manage.py dumpdata users > users/fixtures/initial_data.json --natural --indent=4
