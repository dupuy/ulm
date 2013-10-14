Tests
=====

DBus mocking using python-dbusmock_ is used for all levels of testing,
so that an actual laptop configuration is not required.

.. _python-dbusmock: https://launchpad.net/python-dbusmock

Unit tests are provided for the classes that retrieve information via DBus.
You can run unit tests using make at the top level, or directly with nose or
pytest::

    ulm$ make test
    ...
    Ran 2 tests in 0.410s
    ...
    OK

    ulm$ py.test ulm
    =========================== test session starts ============================
    platform linux2 -- Python 2.7.3 -- pytest-2.4.2
    collected 2 items 
    ...
    =============================  in 0.52 seconds =============================

Integration testing should be done with Django testing framework, and
eventually system testing using django-webtest or maybe Selenium, but these
are not yet implemented.
