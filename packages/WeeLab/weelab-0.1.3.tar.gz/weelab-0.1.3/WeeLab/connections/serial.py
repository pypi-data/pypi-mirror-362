from WeeLab.connections.base import InstrumentConnection


class SerialConnection(InstrumentConnection):
    def __init__(self, port: str, baudrate: int = 9600):
        import serial

        self.ser = serial.Serial(port, baudrate, timeout=1)

    def write(self, command: str):
        self.ser.write((command + "\n").encode())

    def read(self) -> str:
        return self.ser.readline().decode().strip()

    # def read_all(self) -> str:
    #     return self.ser.read_all().decode()

    def read_all(self) -> str:
        lines = []
        while True:
            try:
                line = self.ser.readline().decode().strip()
            except UnicodeDecodeError:
                line = self.ser.readline().decode().strip()
            # line = self.ser.readline().decode().strip()
            if not line:
                break
            lines.append(line)
        return "\n".join(lines)

    def close(self):
        self.ser.close()

    def get_serial_number(self) -> str:
        return self.ser.serial_number if hasattr(self.ser, "serial_number") else None

    def __del__(self):
        self.close()
