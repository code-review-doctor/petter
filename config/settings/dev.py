import dj_database_url

from config.settings.base import *  # noqa: F403

DATABASES = {
    'default': dj_database_url.config(default=env('DATABASE_URL_LOCAL'))  # noqa: F405
}
SECRET_KEY = env('SECRET_KEY')   # noqa: F405
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
