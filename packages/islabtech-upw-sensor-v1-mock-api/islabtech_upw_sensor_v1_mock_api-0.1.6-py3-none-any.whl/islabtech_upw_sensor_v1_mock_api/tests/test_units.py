from islabtech_upw_sensor_v1_mock_api import set_addr_part


def test_set_addr_part():
    addr = "192.0.1.2"
    addr = set_addr_part(addr, 1, 168)
    assert addr == "192.168.1.2"
