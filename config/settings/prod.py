import dj_database_url

from .base import * # noqa

DEBUG = False
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES = {
    'default': db_from_env
}

SECRET_KEY = env('SECRET_KEY', None)  # noqa: F405

ALLOWED_HOSTS = ['petter-island.herokuapp.com', '.herokuapp.com']
