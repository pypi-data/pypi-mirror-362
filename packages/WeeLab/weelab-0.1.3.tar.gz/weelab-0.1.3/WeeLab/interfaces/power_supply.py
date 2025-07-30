from abc import ABC, abstractmethod


class PowerSupply(ABC):
    @abstractmethod
    def set_voltage(self, channel: int, voltage: float): ...
