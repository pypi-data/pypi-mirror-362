from WeeLab.devices.stage import Stage


def test_stage_command(mock_connection):
    stage = Stage(mock_connection)
    stage.move(10, 20)
    stage.ask_position()
    stage.move(1, 2)
    # caen.set_voltage_modulating_ramp(23, 20)
    assert mock_connection.last_command == "move 320 640 "
