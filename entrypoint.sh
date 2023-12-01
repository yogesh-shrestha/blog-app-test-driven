#!bin/ash

echo "Database migrations"
python manage.py migrate

exec "$@"