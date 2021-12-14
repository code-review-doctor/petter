"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.environ.get("DJANGO_ENV") == 'prod':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'
elif os.environ.get("DJANGO_ENV") == 'dev':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'
elif os.environ.get("DJANGO_ENV") == 'test':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'

application = get_asgi_application()
