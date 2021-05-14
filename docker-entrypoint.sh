#!/bin/ash

set -euo pipefail

echo "==> $(date +%H:%M:%S) ==> Migrating Django models..."
python src/manage.py migrate --noinput

echo "==> $(date +%H:%M:%S) ==> Running Gunicorn..."
exec gunicorn -c /app/src/config/gunicorn.py config.wsgi -b ${GUNICORN_BIND_SOCKET} -b 0.0.0.0:${GUNICORN_BIND_PORT} --chdir /app/src/
