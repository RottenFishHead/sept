import os

from django.core.asgi import get_asgi_application

# Use the package-level settings so website/__init__.py can choose base/dev/prod
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website")

application = get_asgi_application()
