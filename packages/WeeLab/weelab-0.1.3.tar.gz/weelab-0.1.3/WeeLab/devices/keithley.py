from WeeLab.connections.base import InstrumentConnection
from WeeLab.interfaces.multimetre import Multimetre

import time

"""A class for interfacing with Keithley Multimeter devices.
This class provides methods to configure the multimeter, measure current and voltage,
and manage the device's settings.

Example usage:
    from WeeLab import KeithleyMultimetre, VisaConnection
    keithley = KeithleyMultimetre(conn=VisaConnection(resource_name='USB0::0x05E6::0x2100::8012509::INSTR'))
    keithley.configure_voltage(0.001, 0.001)
    keithley.configure_current(0.001, 0.001)
    keithley.set_sample_count(100)
    current = keithley.get_current()
    voltage = keithley.get_voltage()
"""


class KeithleyMultimetre(Multimetre):
    def __init__(self, conn: InstrumentConnection):
        """
        Initialize the Keithley Multimeter with a connection.
        :param conn: An instance of InstrumentConnection to communicate with the multimeter
        Example:
        ``` python
        from WeeLab import KeithleyMultimetre, VisaConnection
        keithley = KeithleyMultimetre(
            conn=VisaConnection(resource_name='USB0::0x05E6::0x2100::8012509::INSTR'))
        ```
        """
        self.conn = conn
        self.conn.write('display:text "Welcome @ WeeLab"')
        time.sleep(3)  # Allow time for the display to update
        self.conn.write('display:text:clear')
        self.reset()
    
    def set_sample_count(self, count: int):
        """
        Set the number of samples to be taken.
        :param count: Number of samples
        """
        self.conn.write(f"SAMPLE:COUNT {count}")

    def get_current(self, mode="dc") -> float:
        command = f"MEAS:CURR:{mode}?"
        response = self.conn.query(command)
        return self.process_measurement(response)
    
    def get_voltage(self, mode="dc") -> float:
        """
        Measure voltage on a specified channel.
        :param channel: Channel number to measure voltage from
        :return: Measured voltage as a float
        """
        command = f"MEAS:VOLT:{mode}?"
        response = self.conn.query(command)
        return self.process_measurement(response)
    
    def get_current_range(self, mode="dc", rang=10e-3, res=1e-9) -> float:
        command = f"MEAS:CURR:{mode}? {rang}, {res}"
        response = self.conn.query(command)
        return self.process_measurement(response)
    
    def get_voltage_range(self, mode="dc", rang=10e-3, res=1e-9) -> float:
        """
        Measure voltage on a specified channel.
        :param channel: Channel number to measure voltage from
        :return: Measured voltage as a float
        """
        command = f"MEAS:VOLT:{mode}? {rang}, {res}"
        response = self.conn.query(command)
        return self.process_measurement(response)
    
    def configure_current(self, range: float, resolution: float = 1e-9):
        """
        Configure the multimeter for current measurement.
        :param range: Current range in Amperes
        :param resolution: Resolution in Amperes
        """
        self.conn.write(f"CONFIGURE:CURRENT:DC {range}, {resolution}")
    
    def configure_voltage(self, range: float, resolution: float = 1e-9):
        """
        Configure the multimeter for voltage measurement.
        :param range: Voltage range in Volts
        :param resolution: Resolution in Volts
        """
        self.conn.write(f"CONFIGURE:VOLTAGE:DC {range}, {resolution}")
    
    def set_sample_count(self, count: int):
        """
        Set the number of samples to be taken.
        :param count: Number of samples
        """
        self.conn.write(f"SAMPLE:COUNT {count}")
    
    def set_trigger_count(self, count: int):
        """
        Set the number of triggers to be taken.
        :param count: Number of triggers
        """
        self.conn.write(f"TRIGGER:COUNT {count}")

    def set_trigger_source(self, source: str = "immediate"):
        """
        Set the trigger source.
        :param source: Trigger source (e.g., "bus", "immediate", "external")
        """
        self.conn.write(f"TRIGGER:SOURCE {source}")

    def process_measurement(self, measurement: str) -> float:
        """
        Process the measurement string to extract the float value.
        :param measurement: Measurement string from the multimeter
        :return: Processed float value
        """
        meas_split = measurement.split(",")
        if len(meas_split) == 1:
            return float(meas_split[0].strip())
        elif len(meas_split) > 1:
            return sum(float(i.strip()) for i in meas_split) / len(meas_split)
        else:
            raise ValueError("Invalid measurement format received from the multimeter.")

    def print_id(self):
        idn = self.conn.query("*IDN?")
        print(f"Keithley Multimetre ID: {idn.strip()}")

    def reset(self):
        """
        Reset the Keithley multimeter to its default state.
        """
        self.conn.write("*RST; STATUS:PRES; *CLS")
    
    def query(self, command: str) -> str:
        """
        Send a command to the multimeter and return the response.
        :param command: The command to send
        :return: The response from the multimeter
        """
        return self.conn.query(command).strip()
    
    def write(self, command: str):
        """
        Send a command to the multimeter.
        :param command: The command to send
        """
        self.conn.write(command)
    
    def read(self) -> str:
        """
        Read a response from the multimeter.
        :return: The response from the multimeter
        """
        return self.conn.read().strip()

