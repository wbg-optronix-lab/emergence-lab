"""
WSGI config for wbg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import json
import os
import site
import sys

from django.core.wsgi import get_wsgi_application

# Secrets

_BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(_BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def _get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return exception.
    via Two Scoops of Django 1.6 pg 49
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Setting {0} is missing from the secrets file'.format(setting)
        raise ImproperlyConfigured(error_msg)

# End secrets

if _get_secret('PRODUCTION_MODE') == 'production':
    site.addsitedir('{}/local/lib/python2.7/site-packages'.format(_get_secret('VIRTUAL_ENV_PATH')))

    sys.path.append(_get_secret('SYSTEM_PATH'))
    sys.path.append(os.path.join(_get_secret('SYSTEM_PATH'), _get_secret('SETTINGS_REL_ROOT')))

    activate_env = os.path.expanduser('{}/bin/activate_this.py'.format(_get_secret('VIRTUAL_ENV_PATH')))
    execfile(activate_env, dict(__file__=activate_env))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings.{1}'.format(_get_secret('SETTINGS_REL_ROOT'), _get_secret('PRODUCTION_MODE')))

    application = get_wsgi_application()
else:
    sys.path.append('/var/wsgi')
    sys.path.append('/var/wsgi/wbg')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbg.settings.base')

    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()
