import os

if os.environ.get("DJANGO_ENV") == 'prod':
    from .prod import __all__  # noqa: F403 F401
elif os.environ.get("DJANGO_ENV") == 'dev':
    from .dev import __all__  # noqa: F403 F401
