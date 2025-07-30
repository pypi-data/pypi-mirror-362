# UPW Sensor API

API for the [ISLabTech UPW Sensor](https://gitlab.com/islabtech/upw-sensor)

## REST API
[The entire REST API is documented in OpenAPI/Swagger.](https://gitlab.com/islabtech/upw-sensor/api/-/blob/main/openapi.yml).

## Modbus/TCP
[The Modbus/TCP interface is documented in this PDF.](https://gitlab.com/islabtech/upw-sensor/api/-/raw/main/modbus-doc.pdf?inline=false)

## 🐍 Mock API

Run the mock API locally with Python:

```sh
pip3 install islabtech_upw_sensor_v1_mock_api
python3 -m islabtech_upw_sensor_v1_mock_api
```

Run it with the web app:

```sh
python3 -m islabtech_upw_sensor_v1_mock_api --web-app /path/to/web-app-git-repo
```

Access it with cURL:

```sh
curl -X GET http://localhost:5000/api/v1/measurements/latest
curl -X GET http://localhost:5000/api/v1/system/status
curl -X PATCH http://localhost:5000/api/v1/settings/network/wifi -H "Content-Type: application/json" \
    -d '{"ssid": "my wifi", "password": "my password"}'
```

<!-- ## :book: Documentation

### Guides

Each group of API endoints is documented in its own guide.

- [measure](/guides/measure.md)
- [temperature calibration](/guides/temperature%20calibration.md)
- [conductivity calibration](/guides/conductivity%20calibration.md)

- [system](/guides/system.md)
- [settings](/guides/settings.md) -->
