import time
from WeeLab.connections.base import InstrumentConnection

"""
NktPilasLaser Control Module
This module provides an interface to control the Nkt Pilas laser,
allowing for enabling/disabling the laser, setting the tune, trigger mode,
and frequency, as well as retrieving the status of the laser.
Example usage:
```python
from LabPack.devices.pilas import NktPilasLaser
from LabPack.connections.serial import SerialConnection
pilas = NktPilasLaser(
    conn=SerialConnection(port="COM4", baudrate=19200))
pilas.enable()  # Enable the laser
pilas.set_tune(500)  # Set the tune to 500
pilas.set_trigger_mode("internal")  # Set trigger mode to internal
pilas.set_frequency(20_000_000)  # Set frequency to 20 MHz
status = pilas.get_status()  # Get the status of the laser
"""


class NktPilasLaser:
    def __init__(self, conn: InstrumentConnection):
        """
        Initialize the Nkt Pilas laser.
        :param conn: An instance of InstrumentConnection (e.g., SerialConnection).
        Example:
        ``` python
        from LabPack.devices.pilas import NktPilasLaser
        from LabPack.connections.serial import SerialConnection
        pilas = NktPilasLaser(
            conn=SerialConnection(port="COM4", baudrate=19200))
        ```
        """

        self.conn = conn

    def enable(self):
        self.conn.query("ld=1")

    def disable(self):
        self.conn.query("ld=0")

    def set_tune(self, tune: float):
        if not (0 <= tune <= 999):
            raise ValueError("Tune must be between 0 and 999")
        self.conn.query(f"tune={int(tune)}")

    def set_trigger_mode(self, mode: str):
        if mode not in ["internal", "external"]:
            raise ValueError("Mode must be 'internal' or 'external'")
        if mode == "internal":
            self.conn.query(f"ts=0")
        elif mode == "external":
            self.conn.query(f"ts=2")

    def set_frequency(self, frequency: float):
        if not (0 <= frequency <= 40_000_000):
            raise ValueError("Frequency must be between 0 and 40 MHz")
        self.conn.query(f"f={int(frequency)}")

    def get_status(self) -> str:
        self.conn.write("state?")
        time.sleep(1)  # Allow time for the command to process
        return self.conn.read_all().strip()
