"""
init test parameters

Docs:
- https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=pytest_addoption#pytest.hookspec.pytest_addoption
- https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html#pluginorder
"""


# https://docs.pytest.org/en/7.1.x/example/parametrize.html
def pytest_addoption(parser):
    """processes "--host" and "--port" option to connect to Modbus/TCP server"""
    parser.addoption(
        "--host",
        action="store",
        help="select the host where the Modbus/TCP server runs",
    )
    parser.addoption(
        "--port",
        action="store",
        help="select the port where the Modbus/TCP server listens",
    )
