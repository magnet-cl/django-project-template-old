#!/bin/bash
set -e
LOGFILE=~/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=%(user)s
GROUP=%(user)s
cd %(server_root_dir)s
source .env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec .env/bin/gunicorn_django -w $NUM_WORKERS -b 0.0.0.0:%(django_port)s \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE
