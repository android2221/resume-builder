# Apply database migrations
echo "Waiting for database"
/wait-for-it.sh db:5432

echo "Apply database migrations"
python manage.py makemigrations accounts builder
python manage.py migrate

# Run tests
echo "running tests"
python manage.py test
