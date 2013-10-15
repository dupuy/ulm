# pylint: disable=W0401,W0614,C0111
from .base import *                     # noqa


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Django Admin', 'nobody@localhost'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ulm',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',        # Empty for local domain sockets
                           # or '127.0.0.1' for localhost through TCP.
        'PORT': '',        # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'
