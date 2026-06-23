#!/bin/sh
set -e
echo "Waiting for PostgreSQL database to be online..."
if [ -n "$DATABASE_URL" ]; then
  until nc -z -v -w30 $(echo $DATABASE_URL | sed -r 's/.*@([^:]*):.*/\1/') 5432; do
    echo "Postgres is unavailable - sleeping..."
    sleep 1
  done
  echo "Postgres is up!"
fi
echo "Applying Django database migrations..."
python manage.py migrate --noinput
echo "Starting Gunicorn production server..."
exec gunicorn -c docker/production/gunicorn.conf.py config.wsgi:application
