Deployment
==========

If you want to make this a standard service running on the laptop, you will
probably want to install a webserver with WSGI interface, such as
`apache2+mod-wsgi`_, `gunicorn`_, `nginx+gunicorn`_ or `nginx+uWSGI`_.

.. _`apache2+mod-wsgi`: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/
.. _`gunicorn`: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/gunicorn/
.. _`nginx+gunicorn`: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
.. _`nginx+uWSGI`: https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
