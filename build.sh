#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Gunicorn server
gunicorn ewebsite.wsgi:application --bind 0.0.0.0:8000
