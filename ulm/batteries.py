# -*- coding: utf-8 -*-
# Copyright © 2013 Alexander Dupuy, see ulm/LICENSE

"""Battery status (charge percentage, lifetime).

.. moduleauthor:: Alexander Dupuy <alex.dupuy@mac.com>

The batteries module defines classes that use DBus to retrieve information from
UPower about battery status, such as charge percentage, time remaining, etc.

"""

import datetime
import dbus

# DBus names and paths for UPower / DeviceKit
UP_NAME = 'org.freedesktop.UPower'
UP_PATH = '/org/freedesktop/UPower'
DK_NAME = 'org.freedesktop.DeviceKit.Power'
DK_PATH = '/org/freedesktop/DeviceKit/Power'
PROP_NAME = 'org.freedesktop.DBus.Properties'

BAT_STATES = ['Unknown', 'Charging', 'Discharging', 'Empty', 'Fully charged',
              'Pending charge', 'Pending discharge']


class Battery(object):
    """Battery device.

    :param props: Battery properties
    :type props: dict

    """

    def __init__(self, props):
        """Initialize a new battery."""
        self._name = props['NativePath'].rsplit('/', 1)[1]
        self._update = datetime.datetime.fromtimestamp(props['UpdateTime'])
        self._percentage = "%.0f" % props['Percentage']
        state = props['State']
        self._state = BAT_STATES[state]
        self._remaining = None
        if state == 1:
            self._remaining = props['TimeToFull']
        if state == 2:
            self._remaining = props['TimeToEmpty']

    @property
    def name(self):
        """Battery device name."""
        return self._name

    @property
    def last(self):
        """Integer seconds since last read of device status."""
        return int((datetime.datetime.now() - self._update).total_seconds())

    @property
    def age(self):
        """Device status age string.

        Formatted as timedelta ([D days] H:MM:SS).

        """
        return str(datetime.timedelta(seconds=self.last))

    @property
    def percentage(self):
        """Charge level.

        String, formatted as integer percentage.

        """
        return self._percentage

    @property
    def state(self):
        """Charging state.

        String: one of Unknown, Charging, Discharging, Empty, Fully charged,
        Pending charge, Pending discharge
        

        """
        return self._state

    @property
    def remaining(self):
        """Time remaining until empty/full

        Formatted as timedelta ([D days] H:MM:SS)

        """
        if self._remaining is None:
            return ''
        return str(datetime.timedelta(seconds=self._remaining - self.last))

    def __lt__(self, other):
        """Make batteries orderable."""
        return self.name < other.name

    def __str__(self):
        """Return battery name as string representation."""
        return self.name


class Batteries(object):
    """Battery status from UPower via DBus.

    :param bus: DBus to use instead of dbus.SystemBus()
    :type bus: optional

    The initializer for this class takes an optional bus argument; this allows
    a mocked bus to be used for testing instead of the standard system bus.

    """

    def __init__(self, bus=None):
        self._bats = []
        self._bus = bus or dbus.SystemBus()
        # Get a proxy and interface for UPower or DeviceKit/Power
        try:
            up_proxy = self._bus.get_object(UP_NAME, UP_PATH)
            self.up_name = UP_NAME
            self.up_path = UP_PATH
        except (dbus.DBusException):
            up_proxy = self._bus.get_object(DK_NAME, DK_PATH)
            self.up_name = DK_NAME
            self.up_path = DK_PATH
        self.dev_name = self.up_name + '.Device'
        up_iface = dbus.Interface(up_proxy, self.up_name)

        for device in up_iface.EnumerateDevices():
            # Get a proxy and property interface for the device
            dev_proxy = self._bus.get_object(self.up_name, device)
            dev_props = dbus.Interface(dev_proxy, PROP_NAME)

            # Make sure the device is a battery
            if dev_props.Get(self.dev_name, "Type") != 2:  # Battery==2
                continue

            # Make sure the battery is present
            if not dev_props.Get(self.dev_name, "IsPresent"):
                continue

            dev_dict = dev_props.GetAll(self.dev_name, byte_arrays=True)

            self._bats.append(Battery(dev_dict))

    @property
    def bats(self):
        """Sorted list of batteries"""
        return sorted(self._bats)

    @property
    def bus(self):
        """DBus used to collect information"""
        return self._bus
