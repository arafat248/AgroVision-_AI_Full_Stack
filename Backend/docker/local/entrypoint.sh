#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e
echo "Waiting for PostgreSQL database to be online..."
# Wait for postgres to be ready if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
  # Simple loop to check port 5432
  until nc -z -v -w30 $(echo $DATABASE_URL | sed -r 's/.*@([^:]*):.*/\1/') 5432; do
    echo "Postgres is unavailable - sleeping..."
    sleep 1
  done
  echo "Postgres is up and running!"
fi
echo "Running Django database migrations..."
python manage.py migrate --noinput
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000