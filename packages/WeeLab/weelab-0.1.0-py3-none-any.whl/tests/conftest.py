import pytest
from WeeLab.connections.visa import InstrumentConnection


class MockConnection(InstrumentConnection):
    def __init__(self):
        self.last_command = ""

    def write(self, command: str):
        self.last_command = command

    def read(self) -> str:
        if self.last_command == "C1:WF? DAT1":
            return "MOCK_WAVEFORM_DATA"
        if self.last_command == "currpos ":
            return "currpos 1 1 "
        # return "UNKNOWN_COMMAND"
        return "OK"

    def read_all(self) -> str:
        return "MOCK_READ_ALL_DATA"

    def get_serial_number(self) -> str:
        return "MOCK_SERIAL_NUMBER"

    def close(self):
        pass

    def query(self, command: str) -> str:
        self.write(command)
        return self.read()


@pytest.fixture
def mock_connection():
    return MockConnection()
