#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "PostgreSQL is up and running!"

# Run database migrations
# python manage.py migrate --no-input

# Collect static files (for production only)
# python manage.py collectstatic --no-input

# Create superuser (if not created already)
# python manage.py createsuperuser --noinput || echo "Superuser creation skipped or already exists"

# Start Django server
python manage.py runserver 0.0.0.0:8000

# Keep container running
tail -f /dev/null