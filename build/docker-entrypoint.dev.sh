#!/bin/bash

# Apply database migrations
echo "Waiting for database"
/build/wait-for-it.sh db:5432

echo "Apply database migrations"
python manage.py makemigrations accounts builder
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8001 --insecure
