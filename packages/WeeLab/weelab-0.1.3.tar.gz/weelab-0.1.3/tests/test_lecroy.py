from WeeLab.devices.lecroy9104 import LeCroyWaveRunner


def test_lecroy_waveform_read(mock_connection):
    scope = LeCroyWaveRunner(mock_connection)
    scope.find_scale(1)
    scope.getMeasure(1, "MEAN")
    scope.clear_sweeps()
    assert mock_connection.last_command == "vbs 'app.clearsweeps' "
