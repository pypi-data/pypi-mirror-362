from WeeLab.devices.caen_a7585 import CAEN_A7585


def test_caen_voltage_command(mock_connection):
    caen = CAEN_A7585(mock_connection)
    caen.set_voltage(80)
    # caen.set_voltage_modulating_ramp(23, 20)
    assert mock_connection.last_command == "AT+SET,0,1"
