# Temperature Calibration

The UPW sensor has an inbuilt Pt1000 temperature sensor to measure the water / fluid temperature.

The currently active calibraton parameters can be fetched and modified via the API. For a proper calibration process, however, you want to run a the calibration wizard.

## Live calibration

The currently active temperature calibration can be fetched and modified via the `/api/v1/setting/calibration/temperature` endpoint. See the [API documentation](../openapi.yml) for a formal documentation.

:warning: Do not modify the calibration parameters while they are still in use if you are not 100 % sure. A bad calibration will immediately affect sensor readings. Use the [wizard](#wizard) instead.


## Wizard

The calibration wizard will guide you through the process of calibrating the temperature sensor. All wizard endpoints are formally documented in the [API documentation](../openapi.yml).

### Initialize
The calibration wizard must first be initialized via `/api/v1/settings/calibration/temperature/wizard/start` endpoint. This will discard any previous wizard activities and put the wizard into a defined, fresh state.

### Take calibration points
1. Submerge the sensor electrodes (and the temperature sensor with them) into a liquid (preferrably (ultra-)pure water) with a known temperature.
2. POST the known temperature `/api/v1/settings/calibration/temperature/wizard/points`. The sensor will take a reading and connect it with the temperature.
3. Repeat the process for a different temperature which is at least 10 K different from the first one.
4. Add as many calibration points as you want (2 are usually enough).

If some calibration points need to be edited afterwards, the [API documentation](../openapi.yml) lists all endpoints necessary to edit all calibration points individually.

:information_source: If the calibration temperature is not known at the point when the sensor takes a reading, just POST a dummy value and edit it afterwards. You need to tell the device the correct temperature before [finishing the wizard](#commit-calibration).

### Preview result
Before [applying](#commit-calibration) the new calibration, it might be useful to manually inspect the calibration result.

:warning: As soon as the calibration result is applied, it can not be rolled back.

### Commit calibration
Finally, commit the calibration results via `/api/v1/settings/calibration/temperature/wizard/finish`.

:warning: The calibration can not be rolled back after this operation.<br>
:warning: You probably want to [preview the calibration result](#preview-result) first.


## Trouble Shooting

### I manually changed the calibration parameters and the sensor now reads garbage.
- quick fix: Change the calibration parameters to:
    - resistance at 0 °C: 1000
    - temperature coefficient: 3.851
- proper fix: recalibrate the temperature sensor with the [wizard](#wizard)

### The wizard's preview/commit result shows an error that the calibration points are not plausible.
- make sure that the Pt1000 temperature probe inside the electrodes is fully submerged into the fluid/gas with the known temperature during calibration
- take at least two calibration points at least 10 K apart
- repeat the calibration process
- make sure the sensor is not broken, see [system.md](system.md) for system diagnostics