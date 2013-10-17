Installation
============

Because this package uses python-dbus, which is not built with setup-tools /
distutils, you will either need to:

1. use ``--system-site-packages`` when you create your virtualenv,
2. install python-dbus manually in the virtualenv, 
3. apply the patch provided at
   https://bugs.freedesktop.org/show_bug.cgi?id=55439 to a local copy of
   python-dbus, repackage the tarball and install that, or
4. avoid the use of virtualenv entirely

Once you have dealt with that, you can install this package and its (other)
dependencies with pip::

    $ pip install git+git://github.com/dupuy/ulm.git

You can then run it (for testing purposes) using Django's runserver::

    $ ulm runserver
    Validating models...

    0 errors found
    Django version 1.3.1, using settings 'ulm.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

You can also clone the Git repository and run it from the source directory::

    $ git clone https://github.com/dupuy/ulm.git
    $ cd ulm
    ulm$ pip install -r requirements/local.txt
    ulm$ python manage.py runserver
    Validating models...

For anything more than that, you will want to run it under a real webserver
as described below in the Deployment section.

