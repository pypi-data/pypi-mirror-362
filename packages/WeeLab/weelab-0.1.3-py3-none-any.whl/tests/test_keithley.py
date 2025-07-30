from WeeLab.devices.keithley import KeithleyMultimetre


def test_keithley_voltage_command(mock_connection):
    
    keithley = KeithleyMultimetre(mock_connection)
    keithley.configure_voltage(0.001, 0.001)
    keithley.set_sample_count(100)
    current = keithley.get_current() 
    # caen.set_voltage_modulating_ramp(23, 20)
    assert current == -99.9999, "Expected current measurement to be -99.9999"

