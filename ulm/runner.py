# -*- coding: utf-8 -*-
# Copyright © 2013 Alexander Dupuy, see ulm/LICENSE

"""Distribute / setuptools entry-point for manage.py / django-admin.py.

.. moduleauthor:: Alexander Dupuy <alex.dupuy@mac.com>

This module is used to provide an entry point for Distribute / setuptools and
manage.py to do basic Django operations like syncdb and most importantly,
runserver.

"""

import os
import sys


def main():
    """Run manage.py / django-admin.py commands."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ulm.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
