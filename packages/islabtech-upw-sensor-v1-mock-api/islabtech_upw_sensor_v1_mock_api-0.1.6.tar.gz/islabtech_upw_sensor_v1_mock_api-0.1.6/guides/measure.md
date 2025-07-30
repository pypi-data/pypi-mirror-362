# Taking measurements

The UPW sensor API allows the user to:

- take temperature and conductivity measurements
- read out past measurements

Find the formal specifications of the endpoints mentioned in this document at [../openapi.yml](../openapi.yml).


## Read latest measurements

You can query the latest measurement (often less than 1 second old) via `/api/v1/measurements/latest`. Notice that if the sensor malfunctions, the values may be `null`.

You can fetch the last successful measurement via `/api/v1/measurements/last_successful`. If the sensor is broken and has not yet taken a single successful measurement since it last booted, this endpoint may return `null` values.

### Triggering
These endpoints will not trigger a new measurement. The sensor measures continuously and stores the measurement results in its memory. These endpoints request the stored data. To configure triggering, see the below section [Triggering](#triggering).


## Read entire measurement history

You can read all measurements taken since the sensor has last been turned on. Query `/api/v1/measurements/all` to get all measurements.

### Limitations
- The sensor has a limited amount of memory. It may thus not contain more than a certain number of measurement points (e.g. 1000).
- Turning the device off and on again or rebooting it will erase the measurement history.

### Errors
- The returned arrays may be empty if the sensor just booted or if it is broken and can thus not take any measurements.
- Some of the values in the returned arrays may continue `null` values. These can occur if the sensor malfunctions (either temporarily or permantently).


## Triggering

The sensor takes measurements continuously. It is currently not possible to configure the measure trigger.


## Troubleshooting

The sensor's health status can be checked via the `/api/v1/system/health` and the `/api/v1/system/status` endpoints (documented in [system.md](system.md)).
