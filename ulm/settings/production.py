from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alexander Dupuy', 'alex.dupuy@mac.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ulm',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}