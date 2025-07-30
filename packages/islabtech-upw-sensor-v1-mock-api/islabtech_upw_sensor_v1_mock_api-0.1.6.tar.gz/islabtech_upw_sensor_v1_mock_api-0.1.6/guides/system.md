# System

The UPW sensor runs on a modern microcontroller with rich capabilities like WiFi, Ethernet and Bluetooth. It has modern features, like:
- automatic firmware updates via the internet
- fetching the clock time from a time server
- accessing peripherals like an SD card
- rich logging capabilities

As we try to make all features accessible via the API, there is an entire group of "system" endpoints only for these functions.

:information_source: All endpoints are formally documented in the [API documentation](../openapi.yml).


## Status
TODO

## Health
TODO


## Version
Both hardware and software version can be read via `/api/v1/system/version`. To update the software, see [below](#update-firmware). The hardware serial number can be fetched via the [status](#status).


## Update Firmware
The sensor automatically polls the firmware server for updates except if updates are disabled. However, you can also manually trigger a firmware update via `/api/v1/system/update`. The sensor must be able to connect to the following services in order to successfully update:

- DNS server (see [networking settings](settings.md))
- https://firmware.islabtech.com/

After fetching and installing the firmware update, the sensor will reboot. The measurement data cache (see [measure.md](measure.md)) will be lost upon reboot. Any calibration wizard which is still running will be terminated (see [temperature calibration.md](temperature%20calibration.md) and [conductivity calibration.md](conductivity%20calibration.md)). 

The entire update & reboot process takes approx. 30 seconds.


## Time
TODO

## Reboot
Send a POST request to `/api/v1/reboot` to reboot the device. This will take approx. 10 seconds and the API will not be available during that time.

The measurement data cache (see [measure.md](measure.md)) will be lost upon reboot. Any calibration wizard which is still running will be terminated (see [temperature calibration.md](temperature%20calibration.md) and [conductivity calibration.md](conductivity%20calibration.md)). 


## WiFi Scan
Before configuring the WiFi settings, you can do an access point scan via `/api/v1/system/wifi/scan`.

:information_source: network settings are documented in [settings.md](settings.md)

## Settings
Settings (e.g. network configuration) are documented in their own guide in [settings.md](settings.md).