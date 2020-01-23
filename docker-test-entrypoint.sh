echo "Install pip modules"
pip install -r /requirements/requirements.txt

echo "Change to tests dir"
cd /tests/

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations accounts builder
python manage.py migrate

# Run tests
echo "running tests"
python manage.py test