#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn ke_service.wsgi:application --bind 0.0.0.0:8000
