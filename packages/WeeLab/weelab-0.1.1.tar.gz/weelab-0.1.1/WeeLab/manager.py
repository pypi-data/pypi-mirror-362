from typing import Dict


class DeviceManager:
    def __init__(self):
        self.devices: Dict[str, object] = {}

    def register(self, name: str, device):
        self.devices[name] = device

    def get(self, name: str):
        return self.devices.get(name)
