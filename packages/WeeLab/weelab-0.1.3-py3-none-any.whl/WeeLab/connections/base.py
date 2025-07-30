from abc import ABC, abstractmethod


class InstrumentConnection(ABC):
    @abstractmethod
    def write(self, command: str): ...

    @abstractmethod
    def read(self) -> str: ...

    @abstractmethod
    def read_all(self) -> str: ...

    def query(self, command: str) -> str:
        self.write(command)
        return self.read()
