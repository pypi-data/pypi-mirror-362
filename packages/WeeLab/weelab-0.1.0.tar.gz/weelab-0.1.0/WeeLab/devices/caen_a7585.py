import threading
import time
import serial.tools
from WeeLab.interfaces.power_supply import PowerSupply
from WeeLab.connections.base import InstrumentConnection
from WeeLab.connections.serial import SerialConnection

from colorama import Fore, Style

"""CAEN A7585 Power Supply Control Module for SiPM Biasing.
This module provides an interface to control the CAEN A7585 power supply,
allowing for setting voltage, current, and ramp speed, as well as reading
the current and voltage values.

Example usage:
```python
from LabPack.devices.caen_a7585 import CAEN_A7585
from LabPack.connections.serial import SerialConnection

caen = CAEN_A7585(
    conn=SerialConnection(port="COM6", baudrate=115200))
caen.set_voltage(30)  # Set voltage to 30V
caen.wait_setpoint_reached()  # Wait until the setpoint is reached
caen.get_IV()  # Get the current and voltage values
"""


class CAEN_A7585(PowerSupply):
    def __init__(self, conn: InstrumentConnection, serial_number: str = "0"):
        """
        Initialize the CAEN A7585 power supply.
        :param conn: An instance of InstrumentConnection (e.g., SerialConnection).
        :param serial_number: Serial number of the CAEN A7585 device.
                              If not using InstrumentConnection, this must be provided.

        Example:
        ``` python
        from LabPack.devices.caen_a7585 import CAEN_A7585
        from LabPack.connections.serial import SerialConnection
        caen = CAEN_A7585(
            conn=SerialConnection(port="COM6", baudrate=115200))
        ```
        """

        # self.conn = conn
        self.mutex = threading.Lock()

        self.connected = False
        if isinstance(conn, InstrumentConnection):
            self.conn = conn  # Connection is provided
            self.initialize()
        else:
            if serial_number == "0":  # Neither connection nor serial number provided
                raise ValueError(
                    "Serial number must be provided if not using InstrumentConnection."
                )
            else:  # Connection is not provided, use serial number to connect
                self.connect_no_port(serial_number)

        self.serial_number = self.conn.get_serial_number()

    def initialize(self):
        self.set_machine_mode()
        self.set(0, 0)
        r = self.read_line_with_timeout(1000)
        if "OK" in r:
            self.set(0, 0)  # Turn OFF initially
            self.set(1, 0)  # digital mode
            self.set(3, 5)  # ramp [V/s]
            self.set(2, 20)  # voltage [V]
            self.set(5, 5)  # max current [mA]
            self.set(4, 80)  # max voltage [V]
            time.sleep(0.2)

            self.connected = True
            self.read_all()
            print(
                Fore.GREEN
                + "CAEN HV module A7585 biasing SiPM initialized."
                + Style.RESET_ALL
            )
        else:
            self.conn.close()
            raise Exception(
                "Error: CAEN HV module A7585 biasing SiPM could not be initialized."
            )

    def connect_no_port(self, serial_number: str):
        if not self.connected:
            ports = serial.tools.list_ports.comports()
            exception_msg_list = []
            exception_port_list = []

            available_serial_number = [
                port.serial_number for port in ports if port.serial_number is not None
            ]
            if serial_number not in available_serial_number:
                raise Exception(
                    f"Error: CAEN HV module A7585 biasing SiPM named {serial_number} seems not connected to the computer."
                    f"\nAvailable ones are : {available_serial_number}"
                )

            for port in ports:
                if serial_number:
                    if port.serial_number != serial_number:
                        continue
                try:
                    # print(port.device)
                    # self.serialPort = serial.Serial(
                    #     port=port.device,
                    #     baudrate=115200,
                    #     bytesize=8,
                    #     parity="N",
                    #     stopbits=1,
                    #     timeout=1,
                    # )
                    self.conn = SerialConnection(
                        port=port.device,
                        baudrate=115200,
                    )
                    self.serial_number = port.serial_number
                    self.initialize()
                    break
                except Exception as ex:
                    # print(f"Error connecting to port {port}: {ex}")
                    exception_msg_list.append(ex)
                    exception_port_list.append(port)
            if not self.connected:
                for port, ex in zip(exception_msg_list, exception_port_list):
                    print(f"Error connecting to port {port}: {ex}")
                raise Exception(
                    "Error: CAEN HV module A7585 biasing SiPM could not be accessed"
                )
        self.target_hv = 0

        print(f"CAEN HV {self.serial_number} connected successfully.")

    def set_machine_mode(self):
        self.conn.write("AT+MACHINE")

    def set(self, add, val):
        self.conn.write(("AT+SET," + str(add) + "," + str(val)))

    def get(self, add):
        self.conn.write(("AT+GET," + str(add)))

    def read_all(self):
        return self.conn.read_all()

    def read(self):
        return self.conn.read()

    def read_line_with_timeout(self, timeout_milliseconds):
        line_read = False
        received_line = ""

        def read_from_serial():
            nonlocal line_read, received_line
            with self.mutex:
                received_line = self.read()
            line_read = True

        serial_thread = threading.Thread(target=read_from_serial)
        serial_thread.start()
        serial_thread.join(timeout_milliseconds)
        if serial_thread.is_alive():
            line_read = False
        if line_read:
            return received_line
        else:
            return ""

    def set_enHV(self, bit):
        self.set(0, bit)
        r = self.read_line_with_timeout(1000)
        if r == "":
            print("Timeout error")

    def set_voltage(self, value_V):
        self.target_hv = value_V
        self.set(2, value_V)  # Volts
        r = self.read_line_with_timeout(1000)
        if r == "":
            print("Timeout error")
        self.set_enHV(1)
        self.set_enHV(1)

    def set_voltage_modulating_ramp(self, value_V, SiPM_breakdown):
        self.target_hv = value_V
        self.set(3, 10)  # ramp [V/s]
        if value_V < SiPM_breakdown:
            self.set_voltage(value_V)
        else:
            self.set_voltage(SiPM_breakdown)
            time.sleep(SiPM_breakdown / 10)
            self.set(3, 5)  # ramp [V/s]
            self.set_voltage((SiPM_breakdown + value_V) / 2)
            time.sleep((SiPM_breakdown + value_V) / 2 / 5)
            self.set(3, 2)  # ramp [V/s]
            self.set_voltage(value_V)

    def set_max_current(self):
        self.set(5, 1)  # mA
        r = self.read_line_with_timeout(1000)
        if r == "":
            print("Timeout error")

    def set_ramp_speed(self):
        self.set(3, 5)  # V/s
        r = self.read_line_with_timeout(1000)
        if r == "":
            print("Timeout error")

    def get_IV(self):
        hv_eff_current, hv_eff_voltage = 0, 0
        if self.connected:
            self.read_all()
            self.get(231)
            r = self.read_line_with_timeout(1000)
            if len(r) > 4:
                hv_eff_voltage = float(r[3:-3])
            self.get(232)
            r = self.read_line_with_timeout(1000)
            if len(r) > 4:
                hv_eff_current = float(r[3:-3])
        return hv_eff_current, hv_eff_voltage

    def wait_setpoint_reached(self, target_hv=None):
        iter = 0
        if target_hv is None:
            target_hv = self.target_hv
        while iter < 40:  # 20 seconds
            hv_eff_current, hv_eff_voltage = self.get_IV()
            # self.save_IV(hv_eff_current, hv_eff_voltage)

            if (hv_eff_voltage > (target_hv - 0.2)) & (
                hv_eff_voltage < (target_hv + 0.2)
            ):
                # self.timer_setpoint_reached.cancel()
                print(
                    Fore.GREEN
                    + "Setpoint reached: %.2f µA  %.1f V"
                    % (hv_eff_current * 1e3, hv_eff_voltage)
                    + Style.RESET_ALL
                )
                break
            elif iter == 19:
                print(
                    Fore.RED
                    + "Setpoint NOT reached: %.2f µA  %.1f V"
                    % (hv_eff_current * 1e3, hv_eff_voltage)
                    + Style.RESET_ALL
                )
            iter += 1
            time.sleep(0.5)
