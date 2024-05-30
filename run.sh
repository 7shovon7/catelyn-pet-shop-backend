#!/bin/bash

# Navigate to project directory
cd /root/cps/backend

# Activate virtual environment
source .venv/bin/activate

# Install required modules
pip3 install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Apply DB migration
python3 manage.py migrate

# Start gunicorn server
echo "Starting the server..."
gunicorn catelyn_pet_shop.wsgi:application --bind 0.0.0.0:80 --log-level info >> /var/log/cps-backend/server.log 2>&1