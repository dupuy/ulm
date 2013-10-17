# -*- coding: utf-8 -*-
"""Django URLconf file for ulm"""

from __future__ import unicode_literals

from django.conf import settings
try:
    # pylint: disable=E0611
    from django.conf.urls import patterns, include, url
except (ImportError):                   # Django 1.3 compatibility
    from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.static import static

from ulm.views import laptop, batteries, wifi

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = \
    patterns('',
             url(r'^$', laptop),
             url(r'^batter(?:y|ies)/$', batteries),
             url(r'^(?:wifi|wlan)/$', wifi),
             # Uncomment the next line to enable the admin:
             url(r'^admin/', include(admin.site.urls)),
             ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
