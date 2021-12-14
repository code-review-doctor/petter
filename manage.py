#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    if os.environ.get("DJANGO_ENV") == 'prod':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'
    elif os.environ.get("DJANGO_ENV") == 'dev':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'
    elif os.environ.get("DJANGO_ENV") == 'test':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'

    try:
        command = sys.argv[1]
    except IndexError:
        command = 'help'

    running_test = command == 'test'

    if running_test:
        from coverage import Coverage
        coverage = Coverage()
        coverage.erase()
        coverage.start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if running_test:
        coverage.stop()
        coverage.save()
        covered = coverage.report()
        coverage.xml_report()
        coverage.erase()
        # First Quality gate
        if covered < 40:
            sys.exit(1)


if __name__ == '__main__':
    main()
