Installation
============

Python 2.7 is required, and you have to update to ``pip`` version 20.3.4 to
download packages from PyPI due to deprecation of TLS < 1.2.

The dbus support requires some ``apt`` packages; for Ubuntu 20.04 they are:

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
