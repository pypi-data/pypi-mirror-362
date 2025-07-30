from abc import ABC, abstractmethod


class Multimetre(ABC): 
    @abstractmethod
    def get_current(self, channel: int) -> float: ...
    

# @abstractmethod
# def get_waveform(self): ...
