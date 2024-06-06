#!/bin/sh

echo "Waiting for PostgreSQL to be available..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started. Waiting for database initialization..."

until psql -h db -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "PostgreSQL is up but $DB_NAME database is not yet available - sleeping"
  sleep 1
done

echo "Database $DB_NAME is ready to accept connections"

exec "$@"
