import argparse
import pathlib
from islabtech_upw_sensor_v1_mock_api import run_mock_api

if __name__ == "__main__":
    # parse CLI args
    # doc: https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        prog="UPW Sensor Mock API",
        description="mock REST API for the UPW sensor of ISLabTech",
        epilog="© Ilka Schulz Labortechnik 2023",
    )
    parser.add_argument("-w", "--web-app", type=pathlib.Path)
    arguments = parser.parse_args()
    run_mock_api(arguments.web_app)
