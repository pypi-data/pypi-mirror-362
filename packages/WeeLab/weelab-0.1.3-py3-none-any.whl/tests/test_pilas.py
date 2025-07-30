from WeeLab.devices.pilas import NktPilasLaser


def test_pilas_command(mock_connection):
    pilas = NktPilasLaser(mock_connection)
    # caen.set_voltage(80)
    pilas.disable()
    pilas.set_frequency(1000)
    pilas.set_tune(500)
    pilas.set_trigger_mode("internal")
    pilas.enable()

    assert mock_connection.last_command == "ld=1"
