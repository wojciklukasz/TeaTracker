#!/bin/bash

echo -e "\nRunning migrations...\n"
python manage.py migrate

echo -e "\nStarting the server...\n"
python manage.py runserver 0.0.0.0:8000
exec "$@"