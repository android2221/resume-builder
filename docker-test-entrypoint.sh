# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations accounts builder
python manage.py migrate

# Run tests
echo "running tests"
python manage.py test
