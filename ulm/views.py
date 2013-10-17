# -*- coding: utf-8 -*-
# Copyright © 2013 Alexander Dupuy, see ulm/LICENSE

"""Classes for getting battery status (charge percentage, lifetime).

.. moduleauthor:: Alexander Dupuy <alex.dupuy@mac.com>

The batteries module defines classes that use DBus to retrieve information from
UPower about battery status, such as charge percentage, time remaining, etc.

"""
import datetime

from django.shortcuts import render

from ulm.batteries import Batteries
from ulm.wifi import Wifi


def timestamp():
    """Time that status was collected"""
    return "Status at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def laptop(request):
    """Collect status information for laptop and return HTML response."""

    context = {
        'refresh': 5,
        'timestamp': timestamp(),
        'batteries': sorted(Batteries().bats),
        'wifi': sorted(Wifi().aps),
        }
    return render(request, 'ulm.html', context)


def batteries(request):
    """Collect status information for batteries and return HTML response."""

    context = {
        'refresh': 120,
        'item': '- Batteries',
        'timestamp': timestamp(),
        'batteries': sorted(Batteries().bats),
        }
    return render(request, 'ulm.html', context)


def wifi(request):
    """Collect status information for wifi and return HTML response."""

    context = {
        'refresh': 5,
        'item': '- Wifi',
        'timestamp': timestamp(),
        'wifi': sorted(Wifi().aps),
        }
    return render(request, 'ulm.html', context)
