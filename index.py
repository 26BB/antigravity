import os
import sys

# Add the car_rental_system directory to the Python path
path = os.path.join(os.path.dirname(__file__), 'car_rental_system')
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel serverless functions often look for 'app'
app = application
