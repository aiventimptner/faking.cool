#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "Postgres started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
