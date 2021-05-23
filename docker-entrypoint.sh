#!/usr/bin/env bash

python manage.py makemigrations --merge --noinput
python manage.py migrate

exec "$@"
