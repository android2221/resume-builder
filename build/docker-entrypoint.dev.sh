#!/bin/bash

# Apply database migrations
echo "Waiting for database"
/wait-for-it.sh db:5432

# Make things editable
chmod -R 666 /code/

echo "Apply database migrations"
python manage.py makemigrations accounts builder
python manage.py migrate

# Collect static
echo "Collectng static fles"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8001