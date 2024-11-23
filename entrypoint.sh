#!/bin/sh

# Step 1: Wait for PostgreSQL to be ready
echo "========================================"
echo "Step 1: Waiting for PostgreSQL to be ready..."
echo "========================================"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "✅ PostgreSQL is up and running!"

# Step 2: Run database migrations
echo "========================================"
echo "Step 2: Running database migrations..."
echo "========================================"
if python manage.py migrate --no-input; then
  echo "✅ Database migrations completed successfully!"
else
  echo "❌ Database migration failed. Exiting..."
  exit 1
fi

# Step 3: Run tests
echo "========================================"
echo "Step 3: Running tests..."
echo "========================================"
if python manage.py test; then
  echo "✅ All tests passed successfully!"
else
  echo "❌ Tests failed. Exiting..."
  exit 1
fi

# Step 4: Collect static files (for production only)
echo "========================================"
echo "Step 4: Collecting static files..."
echo "========================================"
if python manage.py collectstatic --no-input; then
  echo "✅ Static files collected successfully!"
else
  echo "❌ Collect static files failed. Exiting..."
  exit 1
fi

# Step 5: Create superuser (if not created already)
echo "========================================"
echo "Step 5: Creating superuser (if needed)..."
echo "========================================"
if python manage.py createsuperuser --noinput; then
  echo "✅ Superuser created successfully (if not already exists)!"
else
  echo "⚠️  Superuser creation skipped or already exists."
fi

# Step 6: Start Django server
echo "========================================"
echo "Step 6: Starting Django server..."
echo "========================================"
if python manage.py runserver 0.0.0.0:8000; then
  echo "✅ Django server started successfully!"
else
  echo "❌ Failed to start Django server. Exiting..."
  exit 1
fi
