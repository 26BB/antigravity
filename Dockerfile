# Use Python 3.12 (required for Django 6.x)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from car_rental_system into /app
# This puts manage.py, config/, accounts/, etc at /app/
COPY car_rental_system/ /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Migrate database and start Gunicorn
# Using sh -c to allow multiple commands
CMD sh -c "python manage.py migrate --noinput && exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 8 --timeout 0 config.wsgi:application"
