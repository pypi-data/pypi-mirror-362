from WeeLab.connections.base import InstrumentConnection


class Vxi11Connection(InstrumentConnection):
    def __init__(self, ip: str):
        import vxi11

        # self.inst = self.rm.open_resource(resource_name)
        self.inst = vxi11.Instrument(ip)

    def write(self, command: str):
        self.inst.write(command)

    def read(self) -> str:
        return self.inst.read()

    def read_all(self) -> str:
        return self.inst.read_all()

    def query(self, command: str) -> str:
        return self.inst.ask(command)
