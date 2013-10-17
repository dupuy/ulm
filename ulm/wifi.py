# -*- coding: utf-8 -*-
# Copyright © 2013 Alexander Dupuy, see ulm/LICENSE

"""WiFi information (available APs).

.. moduleauthor:: Alexander Dupuy <alex.dupuy@mac.com>

The wifi module defines classes that use DBus to retrieve information from
NetworkManager about WiFi interfaces and available networks.

"""

import dbus


# DBus names and paths for Wifi
NM_NAME = 'org.freedesktop.NetworkManager'
NM_PATH = '/org/freedesktop/NetworkManager'
PROP_NAME = 'org.freedesktop.DBus.Properties'
DEV_NAME = 'org.freedesktop.NetworkManager.Device'
WIFI_NAME = 'org.freedesktop.NetworkManager.Device.Wireless'
AP_NAME = 'org.freedesktop.NetworkManager.AccessPoint'


class AP(object):
    """Available AP.

    :param props: AP properties
    :type props: dict
    :param device: Name of device through which this AP is visible
    :type device: optional string
    :param connected: Whether device is connected to this AP
    :type connected: optional boolean

    """

    def __init__(self, props, device=None, connected=False):
        """Initialize a new AP."""
        self._bssid = str(props['HwAddress'])
        self._ssid = props['Ssid']
        self._strength = props['Strength']
        self._device = device if connected else None

    @property
    def bssid(self):
        """AP hardware id"""
        return self._bssid

    @property
    def ssid(self):
        """WiFi network name"""
        return self._ssid

    @property
    def signal(self):
        """AP signal strength

        String formatted as integer percentage

        """
        return str(int(self._strength))

    @property
    def device(self):
        """Device name (if any) connected to this AP"""
        return self._device or ''

    def __lt__(self, other):
        """Make APs orderable."""
        if self.device != other.device:
            if other.device == '':
                return True
            elif self.device == '':
                return False
            else:
                return self.device < other.device
        if self.signal != other.signal:
            if self.signal > other.signal:
                return True
            else:
                return False
        return self.bssid < other.bssid

    def __str__(self):
        """Return SSID name as string representation."""
        return self.ssid + '(' + self.bssid + ')'


class Wifi(object):
    """WiFi status from NetworkManager via DBus.

    :param bus: DBus to use instead of dbus.SystemBus()
    :type bus: optional

    The initializer for this class takes an optional bus argument; this allows
    a mocked bus to be used for testing instead of the standard system bus.

    """

    def __init__(self, bus=None):
        self._aps = []
        self._bus = bus or dbus.SystemBus()
        # Get a proxy and interface for NetworkManager
        nm_proxy = self._bus.get_object(NM_NAME, NM_PATH)
        nm_iface = dbus.Interface(nm_proxy, NM_NAME)

        for device in nm_iface.GetDevices():
            # Get a proxy and property interface for the device
            dev_proxy = self._bus.get_object(NM_NAME, device)
            dev_props = dbus.Interface(dev_proxy, PROP_NAME)

            # Make sure the device is enabled before we try to use it
            if dev_props.Get(DEV_NAME, "State") <= 2:
                continue

            # Make sure the device is a WiFi device
            if dev_props.Get(DEV_NAME, "DeviceType") != 2:  # WiFi==2
                continue

            # Get the user-visible interface name for the device (e.g. wlan0)
            dev_name = dev_props.Get(DEV_NAME, "Interface")

            # Get the associated AP's object path (if any)
            connected_path = dev_props.Get(WIFI_NAME, "ActiveAccessPoint")

            # Get a WiFi interface for the device
            wifi_iface = dbus.Interface(dev_proxy, WIFI_NAME)

            # Get all APs the card can see
            for path in wifi_iface.GetAccessPoints():
                # Get a proxy and property interface for the AP
                ap_proxy = self._bus.get_object(NM_NAME, path)
                ap_props = dbus.Interface(ap_proxy, PROP_NAME)

                ap_dict = ap_props.GetAll(AP_NAME, byte_arrays=True)

                self._aps.append(AP(ap_dict, dev_name, path == connected_path))

    @property
    def aps(self):
        """Sorted list of APs"""
        return sorted(self._aps)

    @property
    def bus(self):
        """DBus used to collect information"""
        return self._bus
