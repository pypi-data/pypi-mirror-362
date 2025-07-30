from WeeLab.connections.base import InstrumentConnection


class VisaConnection(InstrumentConnection):
    def __init__(self, resource_name: str):
        import pyvisa

        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource_name)

    def write(self, command: str):
        self.inst.write(command)

    def read(self) -> str:
        return self.inst.read()
