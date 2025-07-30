from WeeLab.devices.tek_afg import Tektronix_AFG3252


def test_afg_voltage_command(mock_connection):
    afg = Tektronix_AFG3252(mock_connection)
    afg.do_set_voltage_ch1(5)
    afg.set_frequency_ch1(10)
    # caen.set_voltage_modulating_ramp(23, 20)
    assert mock_connection.last_command == "source1:frequency 10.000000"
