#!/bin/bash

# Načtení proměnných prostředí
source .env

# Čekání na databázi
until psql -h "db" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c '\q'; do
  >&2 echo "Postgres je nedostupný - spí"
  sleep 1
done

>&2 echo "Postgres je dostupný - pokračuji"

# Spuštění Uvicorn
exec "$@"
