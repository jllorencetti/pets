"""
WSGI config for pets project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

from os import environ

from decouple import config

from django.core.wsgi import get_wsgi_application

settings_module = config("DJANGO_SETTINGS_MODULE", default="pets.settings.dev")
environ['DJANGO_SETTINGS_MODULE'] = settings_module


application = get_wsgi_application()
