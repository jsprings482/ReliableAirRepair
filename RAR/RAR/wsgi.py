"""
WSGI config for RAR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RAR.settings')

application = get_wsgi_application()
application = DjangoWhiteNoise(application, root=os.path.join(BASE_DIR, "static"))
