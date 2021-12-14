import os

if os.environ.get("DJANGO_ENV") == 'prod':
    from .prod import *  # noqa: F403 F401
elif os.environ.get("DJANGO_ENV") == 'dev':
    from .dev import *  # noqa: F403 F401
