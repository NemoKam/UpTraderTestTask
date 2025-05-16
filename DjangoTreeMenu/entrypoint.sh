#! /usr/bin/env bash

sleep 5 && \
    python3 manage.py migrate --no-input && \
    python3 manage.py collectstatic --no-input && \
    python3 manage.py initialize && \
    python3 manage.py loaddata filling/menuitem.json && \
    gunicorn DjangoTreeMenu.wsgi:application --bind 0.0.0.0:8000 --timeout 900
