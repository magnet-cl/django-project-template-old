#!/bin/bash

createdb -E UTF8 template_postgis
createlang -d template_postgis plpgsql

PGSHARE=`pg_config --sharedir`
PGSQL=`find $PGSHARE -name postgis.sql -o -name postgis-32.sql | tail -n 1`
PGSQLSP=`find $PGSHARE -name spatial_ref_sys.sql | tail -n 1`

# Allows non-superusers the ability to create from this template
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"

psql -d template_postgis -f $PGSQL
psql -d template_postgis -f $PGSQLSP

psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
