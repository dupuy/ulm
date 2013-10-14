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

