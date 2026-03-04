# Use Python 3.12 (required for Django 6.x)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set working directory
WORKDIR /app

# Install dependencies from repo root
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the Django project files (car_rental_system/) into /app
COPY car_rental_system/ /app/

# Collect static files (manage.py is now at /app/manage.py)
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 8 --timeout 0 config.wsgi:application
