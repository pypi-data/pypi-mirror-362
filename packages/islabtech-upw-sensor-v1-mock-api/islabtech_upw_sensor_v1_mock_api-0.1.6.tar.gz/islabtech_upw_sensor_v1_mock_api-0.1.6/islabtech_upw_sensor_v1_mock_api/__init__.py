import sys
import json
import time
import math
import argparse
import pathlib
from typing import Optional
from dataclasses import dataclass
import datetime
import random
import logging
import threading

# simulated measurements
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# REST
import flask
from flask import Flask, send_from_directory
from flask_sock import Sock
from simple_websocket.ws import Base as WSBase

# Modbus
import pyModbusTCP
from pyModbusTCP.server import ModbusServer, DataHandler
from pyModbusTCP import constants as ModbusConstants

# constants
MIME_PLAINTEXT_UTF8 = "text/plain;charset=UTF-8"
FIRMWARE_VERSION = "0.1.2"
HARDWARE_VERSION = "1.6.0"
SERIAL_NUMBER = "0123-4567-890A-BCDE"
BROKEN = random.random() < 0.1
if BROKEN:
    print('The device is "broken" and will not perform proper measurements')

# state (more state defined below after type definitions)
random.seed()
measurement_streams: list[WSBase] = []
web_app_path: Optional[str] = None
started_timestamp = datetime.datetime.now() - datetime.timedelta(
    seconds=8 + random.random() * 3
)
last_firmware_update_check = None
automatic_firmware_updates_enabled: bool = True


# code for fake measurements
@dataclass
class Measurement:
    """a single measruement holding physical data (°C / µS/cm), not raw data"""

    timestamp: datetime.datetime
    conductivity: Optional[float]
    temperature: Optional[float]


measurements: list[Measurement] = []


def measure():
    """performs a fake measurement"""
    if BROKEN:
        return
    if len(measurements) == 0:
        measurements.append(
            Measurement(
                datetime.datetime.now(),
                random.random() * 3 + 0.055,
                random.random() * 70 + 10,
            )
        )
    else:
        measurements.append(
            Measurement(
                timestamp=datetime.datetime.now(),
                conductivity=(
                    (None if random.random() < 0.9 else random.random() * 3 + 0.055)
                    if measurements[-1].conductivity is None
                    else (
                        None
                        if random.random() < 0.025
                        else (
                            measurements[-1].conductivity
                            * (0.9 + 0.2 * random.random())
                        )  # drifting value
                        * 0.99
                        + 0.01 * 1  # tend towards a conductivity of 1
                    )
                ),
                temperature=(
                    (None if random.random() < 0.9 else random.random() * 70 + 10)
                    if measurements[-1].temperature is None
                    else (
                        None
                        if random.random() < 0.025
                        else (
                            measurements[-1].temperature
                            * (0.99 + 0.02 * random.random())
                        )  # drifting value
                        * 0.99
                        + 0.01 * 45  # tend towards a temperature of 45
                    )
                ),
            )
        )
    if len(measurements) > 10000:
        measurements.pop(0)
    m = measurements[-1]

    global measurement_streams
    measurement_streams = list(
        filter(lambda client: client.connected, measurement_streams)
    )
    for client in measurement_streams:
        client.send(
            json.dumps(
                {
                    "epoch_timestamp": math.floor(m.timestamp.timestamp()),
                    "epoch_microseconds": m.timestamp.microsecond,
                    "temperature": m.temperature,
                    "conductivity": m.conductivity,
                }
            )
        )


executors = {"default": ThreadPoolExecutor(16), "processpool": ProcessPoolExecutor(4)}
sched = BackgroundScheduler(timezone="Europe/Berlin", executors=executors)
sched.add_job(measure, "interval", seconds=1)


# mock API handlers
app = Flask(__name__)
sock = Sock(app)


# web app
def not_web_app():
    """prepares 500 HTTP response stating that web app is not configured"""
    retval = flask.make_response(
        "mock api is not configured to serve web app\n",
        500,
    )
    retval.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
    return retval


@app.get("/")
def get_web_app_root():
    if web_app_path is not None:
        return send_from_directory(web_app_path, "index.html")
    else:
        return not_web_app()


@app.get("/<path:path>")
def get_web_app(path):
    if web_app_path is not None:
        return send_from_directory(web_app_path, path)
    else:
        return not_web_app()


@app.get("/api/v1/measurements/latest")
def latest_measurement():
    return flask.jsonify(
        {
            "epoch_timestamp": math.floor(measurements[-1].timestamp.timestamp()),
            "epoch_microseconds": measurements[-1].timestamp.microsecond,
            "temperature": measurements[-1].temperature,
            "conductivity": measurements[-1].conductivity,
        }
        if len(measurements) > 0
        else None
    )


@app.get("/api/v1/measurements/latest_successful")
def last_successful_measurement():
    last = next(
        x
        for x in reversed(measurements)
        if x.conductivity is not None and x.temperature is not None
    )
    return flask.jsonify(
        {
            "epoch_timestamp": math.floor(last.timestamp.timestamp()),
            "epoch_microseconds": last.microseconds,
            "temperature": last.temperature,
            "conductivity": last.conductivity,
        }
        if last is not None
        else None
    )


@app.get("/api/v1/measurements/history")
def all_measurements():
    return flask.jsonify(
        list(
            map(
                lambda t: {
                    "epoch_timestamp": math.floor(t.timestamp.timestamp()),
                    "epoch_microseconds": t.timestamp.microseconds,
                    "temperature": t.temperature,
                    "conductivity": t.conductivity,
                },
                measurements,
            ),
        ),
    )


@sock.route("/api/v1/measurements/stream")
def register_measurements_stream(ws: WSBase):
    measurement_streams.append(ws)
    while True:
        time.sleep(1.0)
        if not ws.connected:
            print("WS not connected anymore")
            try:
                measurement_streams.remove(ws)
            finally:
                return  # pylint: disable=return-in-finally,lost-exception


# =================================================================
# System
# =================================================================


@app.post("/api/v1/system/update")
def update():
    """
    checks for a firmware upgrade and will potentially restart the sensor

    TODO:
        - may use different response codes when the firmware is up to date or it is upgraded
    """

    if random.random() < 0.25:
        retval = flask.make_response(
            "an error occured during update\n",
            500,
        )
        retval.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return retval
    else:
        if random.random() < 0.5:
            last_firmware_update_check = datetime.datetime.now()
            return "already up to date\n", {"Content-Type": MIME_PLAINTEXT_UTF8}
        else:
            time.sleep(9 + random.random(6))
            measurements.clear()
            return "successfully updated – rebooting now\n", {
                "Content-Type": MIME_PLAINTEXT_UTF8
            }


@app.get("/api/v1/system/version")
def version():
    return {
        "firmware": {
            "version": "0.1.2",
            "author_name": "Ilka Schulz",
            "author_email": "ilka@islabtech.com",
        },
        "hardware": {
            "version": "0.4.5",
            "serial_number": "0123-4567-89AB-CDEF",
        },
    }


@app.get("/api/v1/system/status")
def system_status():
    return {
        "firmware": {
            "version": "0.1.2",
            "author_name": "Ilka Schulz",
            "author_email": "ilka@islabtech.com",
            "updates": {
                "enabled": automatic_firmware_updates_enabled,
                #  json.set("firmware/updates/pending", TODO);
                "last_check_epoch_timestamp": last_firmware_update_check,
            },
        },
        "hardware": {
            "version": "0.4.5",
            "serial_number": "0123-4567-89AB-CDEF",
        },
        "time": {
            "milliseconds_since_boot": int(
                (datetime.datetime.now() - started_timestamp).total_seconds() * 1000
            ),
            "seconds_since_boot": int(
                (datetime.datetime.now() - started_timestamp).total_seconds()
            ),
            "epoch_time": int(datetime.datetime.now().timestamp()),
            "time_string": datetime.datetime.now().strftime(
                "%A, %d. %B %Y, %T"
            ),  # TODO: test
            # "time_zone_name": "Europe/Berlin",  # TODO: implement
            # "clock_out_of_sync", TODO,
        },
        "network": {
            "ethernet": {
                "connected": True,
                "mac_address": "00:11:22:33:44:55",
                "ipv4_address": "127.0.0.123",
                "ipv6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "speed_mbits": "1000",
                "full_duplex": True,
                # TODO: internet access
            },
            "wifi": {
                "connected": True,
                "mac_address": "66:77:88:99:AA:BB",
                "ipv4_address": "127.0.0.321",
                "ipv6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                #  TODO: internet access
                "ssid": "some wifi",
            },
        },
        # "battery": {
        #     "attached": True,
        #     "state_of_charge_percent": 75,
        # },
        # "sd_card": {"attached": True, "healthy": True, "requires_formatting": False},
    }


@app.post("/api/v1/system/reboot")
def reboot():
    return "Device will reboot now...\n"


@app.get("/api/v1/system/logs/full")
def get_logs_full():
    return "currently not implemented\n"  # TODO: implement


# =================================================================
# Settings
# =================================================================


def patch_settings(settings_object: object, settings: object):
    """PATCH handler for setting objects"""
    # pylint: disable=unidiomatic-typecheck
    for key, value in settings.items():
        if key in settings_object.__dict__.keys():
            # check that types are equal or compatible
            if type(value) == type(settings_object.__dict__[key]) or (
                (type(value) == int or type(value) == float)
                and (
                    type(settings_object.__dict__[key]) == int
                    or type(settings_object.__dict__[key]) == float
                )
            ):
                settings_object.__dict__[key] = value
            else:
                return flask.make_response(
                    f"{key} is not of type {type(settings_object.__dict__[key])}\n",
                    400,
                )
        else:
            retval = flask.make_response("invalid key: " + key + "\n", 400)
            retval.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
            return retval
    print(settings)
    return settings_object.__dict__


# =================================================================
# WiFi settings
# =================================================================
@dataclass
class WiFiSettings:
    connect_to_ap: bool
    ssid: str
    # bssid: str
    user: str
    password: str


wifi_settings = WiFiSettings(
    connect_to_ap=True,
    ssid="some wifi",
    # bssid="00:11:22:33:44:55",
    user="user",
    password="password",
)


@app.get("/api/v1/settings/network/wifi")
def get_wifi_settings():
    return wifi_settings.__dict__


@app.patch("/api/v1/settings/network/wifi")
def patch_wifi_settings():
    return patch_settings(wifi_settings, flask.request.get_json())


# @app.get("/api/v1/system/wifi/scan")
# def wifi_scan():
#     time.sleep(3 + random.random() * 3)
#     return {
#         "wifi_networks": [
#             {
#                 "ssid": "some wifi",
#                 "bssid": "66:77:88:99:AA:BB",
#                 "channel": 1,
#                 "rssi": -80,
#                 "security": "WPA2",  # TODO: this should not be a string but an enum
#             },
#             {
#                 "ssid": "another wifi",
#                 "bssid": "77:88:99:AA:BB:CC",
#                 "channel": 2,
#                 "rssi": -70,
#                 "security": "WPA2",
#             },
#             {
#                 "ssid": "yet another wifi",
#                 "bssid": "88:99:AA:BB:CC:DD",
#                 "channel": 3,
#                 "rssi": -60,
#                 "security": "WPA2",
#             },
#         ]
#     }

# =================================================================
# Ethernet settings
# =================================================================


@dataclass
class EthernetSettings:
    use_dhcp: bool
    ipv4_address: Optional[str]
    ipv4_netmask: Optional[str]
    ipv4_gateway_address: Optional[str]
    dns_server_address_1: str
    dns_server_address_2: str


ethernet_settings = EthernetSettings(
    use_dhcp=True,
    ipv4_address="192.168.0.123",
    ipv4_netmask="255.255.255.0",
    ipv4_gateway_address="192.168.0.1",
    dns_server_address_1="192.168.0.32",
    dns_server_address_2="8.8.8.8",
)


@app.get("/api/v1/settings/network/ethernet")
def get_ethernet_settings():
    return ethernet_settings.__dict__


@app.patch("/api/v1/settings/network/ethernet")
def patch_ethernet_settings():
    return patch_settings(ethernet_settings, flask.request.get_json())


# =================================================================
# NTP settings
# =================================================================


@dataclass
class NtpSettings:
    ntp_server_name_1: str
    ntp_server_name_2: str
    ntp_server_name_3: str


ntp_settings = NtpSettings("pool.ntp.org", "time.fu-berlin.de", "")


@app.get("/api/v1/settings/network/ntp")
def get_ntp_settings():
    return ntp_settings.__dict__


@app.patch("/api/v1/settings/network/ntp")
def patch_ntp_settings():
    return patch_settings(ntp_settings, flask.request.get_json())


# # =================================================================
# # Time settings
# # =================================================================


# @dataclass
# class TimeSettings:
#     time_zone: int
#     time_zone_dst: Optional[int]


# time_settings = TimeSettings(time_zone=100, time_zone_dst=200)


# @app.get("/api/v1/settings/time")
# def get_time_settings():
#     return time_settings.__dict__


# @app.patch("/api/v1/settings/time")
# def patch_time_settings():
#     return patch_settings(time_settings, flask.request.get_json())


# @app.get("/api/v1/system/time")
# def get_time():
#     return {
#         "epoch_time": int(datetime.datetime.now().timestamp()),
#         "time_string": datetime.datetime.now().strftime(
#             "%A, %d. %B %Y, %T"
#         ),  # TODO: test
#         "current_time_zone": time_settings.time_zone
#         if datetime.datetime.now().dst() == 0
#         else time_settings.time_zone_dst,
#     }


# # TODO
# # @app.post("/api/v1/system/time")
# # def set_time():


# =================================================================
# Temperature calibration settings
# =================================================================


@dataclass
class TemperatureCalibration:
    resistance_at_0_C: float
    resistance_coefficient: float


temperature_calibration = TemperatureCalibration(
    resistance_at_0_C=998.2, resistance_coefficient=3.851
)


@app.get("/api/v1/settings/calibration/temperature")
def get_temperature_calibration():
    return temperature_calibration.__dict__


@app.patch("/api/v1/settings/calibration/temperature")
def patch_temperature_calibration():
    return patch_settings(temperature_calibration, flask.request.get_json())


@app.post("/api/v1/settings/calibration/temperature/calibrate")
def calibrate_temperature():
    if "correct_temperature" not in flask.request.get_json():
        response = flask.make_response(
            "user error: please specify the `correct_temperature` " "parameter\n", 400
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    correct_temperature = flask.request.get_json()["correct_temperature"]
    if type(correct_temperature) != type(float):
        response = flask.make_response(
            "user error: the `correct_temperature` parameter must " "be a number\n", 400
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    if random.random() < 0.1:
        response = flask.make_response(
            "internal error: can not update calibration\n", 500
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    temperature_calibration.resistance_at_0_C = 1000.0 + random.random() * 5.0


# =================================================================
# Conductivity calibration settings
# =================================================================


@dataclass
class ConductivityCalibration:
    cell_constant: float


conductivity_calibration = ConductivityCalibration(1.23)


@app.get("/api/v1/settings/calibration/conductivity")
def get_conductivity_calibration():
    return conductivity_calibration.__dict__


@app.put("/api/v1/settings/calibration/conductivity")
def patch_conductivity_calibration():
    return patch_settings(conductivity_calibration, flask.request.get_json())


# TODO: this function is mostly not DRY
@app.post("/api/v1/settings/calibration/conductivity/calibrate")
def calibrate_conductivity():
    if "correct_conductivity" not in flask.request.get_json():
        response = flask.make_response(
            "user error: please specify the `correct_conductivity` " "parameter\n", 400
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    correct_conductivity = flask.request.get_json()["correct_conductivity"]
    if type(correct_conductivity) != type(float):
        response = flask.make_response(
            "user error: the `correct_conductivity` parameter must " "be a number\n",
            400,
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    if random.random() < 0.1:
        response = flask.make_response(
            "internal error: can not update calibration\n", 500
        )
        response.headers.set("Content-Type", MIME_PLAINTEXT_UTF8)
        return response
    conductivity_calibration.cell_constant = 2.4 + random.random(0.2)


def run_flask():
    app.run(debug=True, use_reloader=False)


def single_bit_response(value: bool, count: int):
    logging.info(f"count: {count}")
    array = [False] * count
    array[0] = value
    logging.info(f"response: {array}")
    return DataHandler.Return(exp_code=pyModbusTCP.constants.EXP_NONE, data=array)


def get_digital(addr: int) -> bool:
    """
    Raises:
        IndexError: invalid address
    """
    if addr == 10:
        try:
            return measurements[-1].conductivity < 1.1
        except (IndexError, TypeError):
            return False
    # if addr == 11:
    #     TODO
    elif addr == 20:
        try:
            return measurements[-1].temperature < 25
        except (IndexError, TypeError):
            return False
    # elif addr == 21 or addr == 31:
    #     TODO
    elif addr == 100:
        return wifi_settings.connect_to_ap
    # elif addr == 200:
    #     return ethernet_settings.connect_to_network
    elif addr == 201:
        return ethernet_settings.use_dhcp
    elif addr == 300:
        return automatic_firmware_updates_enabled

    logging.debug(f"invalid address: {addr}, returning error")
    raise IndexError


def get_analog(addr: int) -> int:
    """
    Raises:
        IndexError: invalid address
        ValueError: value not available
    """
    if addr == 10:
        try:
            value = measurements[-1].conductivity * 1000  # nS/cm
            print(f"returning cond={value}")
            return value
        except IndexError:
            raise ValueError
    # elif addr == 11:
    #     TODO
    elif addr == 20:
        try:
            return measurements[-1].temperature * 100  # 100th °C
        except IndexError:
            raise ValueError
    # elif addr == 21:
    #     TODO
    elif addr == 30:
        try:
            return (measurements[-1].temperature + 273.15) * 10
        except IndexError:
            raise ValueError
    # elif addr == 31:
    #     TODO
    elif 210 <= addr <= 213:
        return int(ethernet_settings.ipv4_address.split(".")[addr - 210], 10)
    # elif addr == 220:
    #     TODO: netmask
    elif 230 <= addr <= 233:
        return int(ethernet_settings.ipv4_gateway_address.split(".")[addr - 230], 10)
    elif 240 <= addr <= 243:
        return int(ethernet_settings.dns_server_address_1.split(".")[addr - 240], 10)
    elif 250 <= addr <= 253:
        return int(ethernet_settings.dns_server_address_2.split(".")[addr - 250], 10)
    elif 310 <= addr <= 312:
        return int(FIRMWARE_VERSION.split(".")[addr - 310], 10)
    elif 320 <= addr <= 322:
        return int(HARDWARE_VERSION.split(".")[addr - 320], 10)
    elif 330 <= addr <= 333:
        return int(SERIAL_NUMBER.split("-")[addr - 330], 16)

    logging.debug(f"invalid address: {addr}, returning error")
    raise IndexError


def set_digital(addr: int, value: bool) -> None:
    """
    Raises:
        IndexError: invalid address
        ValueError: value is not a bool
    """
    if not isinstance(value, bool):
        raise ValueError
    if addr == 100:
        wifi_settings.connect_to_ap = value
    # elif addr == 200:
    #     ethernet_settings.connect_to_network = value
    elif addr == 201:
        ethernet_settings.use_dhcp = value
    elif addr == 300:
        global automatic_firmware_updates_enabled  # pylint: disable=global-statement
        automatic_firmware_updates_enabled = value
    else:
        raise IndexError


def set_addr_part(addr: str, part: int, value: int) -> str:
    """sets a part of an IPv4 address
    Parameters:
        addr:  the address string to manipulate, e.g. "192.168.1.2"
        part:  0-based index of the part which shall be changed
        value: the new value of that part. should be 0..255

    Example:
    ```
        addr = "192.0.1.2"
        addr = set_addr_part(addr, 1, 168)
        assert addr == "192.168.1.2"
    ```
    """
    parts: list[str] = addr.split(".")
    print(f"parts: {parts}")
    parts[part] = str(value)
    addr = ".".join(parts)
    return addr


def set_analog(addr: int, value: int) -> None:
    """
    Raises:
        IndexError: invalid address
        ValueError: value is not an int or out of range
    """
    if not isinstance(value, int):
        raise ValueError
    if addr == 10:
        if value < 30 or value > 5500:
            raise ValueError
        conductivity_calibration.cell_constant = 2.4 + random.random(0.2)
    elif addr == 20:
        if value < 0 or value > 100 * 100:  # max: 100 °C in c°C
            raise ValueError
        temperature_calibration.resistance_at_0_C = 990 + random.random(20)
    elif 210 <= addr <= 213:
        if value < 0 or value > 255:
            raise ValueError
        ethernet_settings.ipv4_address = set_addr_part(
            ethernet_settings.ipv4_address, addr - 210, value
        )
    # elif addr == 220:
    #     TODO: netmask
    elif 230 <= addr <= 233:
        if value < 0 or value > 255:
            raise ValueError
        ethernet_settings.ipv4_gateway_address = set_addr_part(
            ethernet_settings.ipv4_gateway_address, addr - 230, value
        )
    elif 240 <= addr <= 243:
        if value < 0 or value > 255:
            raise ValueError
        ethernet_settings.dns_server_address_1 = set_addr_part(
            ethernet_settings.dns_server_address_1, addr - 230, value
        )
    elif 250 <= addr <= 253:
        if value < 0 or value > 255:
            raise ValueError
        ethernet_settings.dns_server_address_2 = set_addr_part(
            ethernet_settings.dns_server_address_2, addr - 230, value
        )
    else:
        raise IndexError


class ModbusHandler(DataHandler):
    """handles read/write Modbus requests"""

    # ========== read ==========
    def read_d_inputs(self, address, count, srv_info):
        return self.read_coils(address=address, count=count, srv_info=srv_info)

    def read_coils(self, address, count, srv_info):
        logging.debug(f"reading coil {address}")
        try:
            array = [False] * count
            for i in range(count):
                array[i] = get_digital(address + i)
            return DataHandler.Return(exp_code=ModbusConstants.EXP_NONE, data=array)
        except IndexError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_ADDRESS)

    def read_i_regs(self, address, count, srv_info):
        logging.debug(f"fetching analog {address}")
        try:
            array = [0] * count
            for i in range(count):
                value = int(get_analog(address + i))
                array[i] = value
            return DataHandler.Return(exp_code=ModbusConstants.EXP_NONE, data=array)
        except IndexError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_ADDRESS)
        except ValueError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_SLAVE_DEVICE_BUSY)

    def read_h_regs(self, address, count, srv_info):
        return self.read_i_regs(address=address, count=count, srv_info=srv_info)

    # ========== write ==========
    def write_coils(self, address, bits_l, srv_info):
        try:
            bits = [bool(b) for b in bits_l]
            for i, b in enumerate(bits):
                set_digital(address + i, b)
            return DataHandler.Return(exp_code=ModbusConstants.EXP_NONE)
        except IndexError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_ADDRESS)
        except ValueError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_VALUE)

    def write_h_regs(self, address, words_l, srv_info):
        try:
            words = [int(i) for i in words_l]
            for i, w in enumerate(words):
                set_analog(addr=address + i, value=w)
            return DataHandler.Return(exp_code=ModbusConstants.EXP_NONE)
        except IndexError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_ADDRESS)
        except ValueError:
            return DataHandler.Return(exp_code=ModbusConstants.EXP_DATA_VALUE)


def run_modbus():
    PORT = 1502
    # TODO: DeviceIdentification
    logging.info(f"starting Modbus/TCP server on port {PORT}")
    server = ModbusServer(
        host="localhost",
        port=PORT,
        data_hdl=ModbusHandler(),
        # TODO: ext_engine=
        # no_block=True
    )
    server.start()


def run_mock_api(arg_web_app_path: Optional[str]):
    # logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARN)
    logging.getLogger("pyModbusTCP.server").setLevel(logging.DEBUG)

    # use CLI arguments
    global web_app_path
    web_app_path = arg_web_app_path
    logging.warning(f"web app path: {web_app_path}")

    # background tasks (simulate measurements)
    sched.start()

    # REST / WebSocket API
    t_rest = threading.Thread(target=run_flask, daemon=True)
    t_rest.start()

    # ModBus server
    t_modbus = threading.Thread(target=run_modbus, daemon=True)
    t_modbus.start()

    # join tasks
    t_rest.join()
    t_modbus.join()

    sys.exit(0)
