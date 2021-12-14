from .base import *  # noqa: F403 F401

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'github_actions',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
SECRET_KEY = 'test12312312asd'   # noqa: F405
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
