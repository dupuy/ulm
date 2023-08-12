Ubuntu Laptop Monitoring (ulm)
==============================

This is a simple Django project that displays battery and WiFi status.

The project uses DBus to gather information from UPower and NetworkManager -
while DBus is over-engineered and annoying, it provides a very high-level
interface (including battery history and time remaining estimation for
UPower, and full SSID list for NetworkManager - even when connected and
running without root privilege).  It should hopefully be less prone to
bit-rot than scraping ``/sys/class/power_supply/*`` files, parsing the
output of ``iwscan`` and so forth.

While using the pygi (GObject Introspection for Python) interface for
NetworkManager would be less painful than using the DBus interfaces, we'd
still need DBus for UPower, and the GObject libraries could drag in GNOME
dependencies that wouldn't otherwise be necessary.

On a system using ``wicd`` for network connection management, the rather
limited DBus interface that it provides doesn't offer anything useful, so
using ``iwscan`` would be more tempting, but it would be much slower.

Instead of UPower, earlier versions of Linux power management support a
mostly compatible DeviceKit/Power DBus API, which is supported (although
untested).  Very old Ubuntu (<9.10) used the rather different HAL DBus API,
that is not supported.

Installation
============

Python 2.7 is required, and you have to update to `pip` version 20.3.4 to
download packages from PyPI due to deprecation of TLS < 1.2.

The dbus support requires some `apt` packages; for Ubuntu 20.04 they are:

- build-essential
- libpython2-dev
- libdbus-1-dev

These should be installed first.

You can install this package and its dependencies with pip::

    $ pip2 install git+https://github.com/dupuy/ulm.git

You can then run it (for testing purposes) using Django's runserver::

    $ ulm runserver
    Validating models...

    0 errors found
    Django version 1.11.29, using settings 'ulm.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

You can also clone the Git repository and run it from the source directory::

    $ git clone https://github.com/dupuy/ulm.git
    $ cd ulm
    ulm$ pip2 install -r requirements/local.txt
    ulm$ python2 manage.py runserver
    Validating models...

For anything more than that, you will want to run it under a real webserver
as described below in the Deployment section.

Deployment
==========

If you want to make this a standard service running on the laptop, you will
probably want to install a webserver with WSGI interface, such as
`apache2+mod-wsgi`_, `gunicorn`_, `nginx+gunicorn`_ or `nginx+uWSGI`_.

.. _`apache2+mod-wsgi`: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/
.. _`gunicorn`: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/gunicorn/
.. _`nginx+gunicorn`: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
.. _`nginx+uWSGI`: https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

Eventually, some or all of these may have the necessary configuration files
provided as part of this repository.

Note
====

I wrote this as a programming challenge in 2013 when I was applying for a
position at Lite Elements (a subsidiary of Deutsche Telekom in Berlin).
It is written using Python 2.7, and as I don't have a laptop or a real
need for this project, I won't be porting it to Python 3. I have updated it
to the most recent versions of packages that still support Python 2.7, which
closed all dependabot security alerts as of 2023-08-12 (~10 years later).
