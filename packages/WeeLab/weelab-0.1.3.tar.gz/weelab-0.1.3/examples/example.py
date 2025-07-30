from abc import ABC, abstractmethod
from typing import Dict
import logging


from WeeLab.const import *
from WeeLab.connections.serial import SerialConnection
from WeeLab.connections.visa import VisaConnection
from WeeLab.connections.vxi11conn import Vxi11Connection
from WeeLab.devices.tek_afg import Tektronix_AFG3252
from WeeLab.devices.caen_a7585 import CAEN_A7585
from WeeLab.devices.lecroy9104 import LeCroyWaveRunner
from WeeLab.devices.pilas import NktPilasLaser
from WeeLab.manager import DeviceManager


# ---------------- Example Setup ----------------
def initialize_devices():
    manager = DeviceManager()

    lecroy_conn = Vxi11Connection(LECROY_IP)
    nkt_conn = SerialConnection(PILAS_COM)
    caen_conn = SerialConnection(CAEN_COM)
    tektronix_conn = VisaConnection(TEKTRONIX_ID)

    manager.register("lecroy", LeCroyWaveRunner(lecroy_conn))
    manager.register("nkt", NktPilasLaser(nkt_conn))
    manager.register("caen", CAEN_A7585(caen_conn))
    manager.register("afg", Tektronix_AFG3252(tektronix_conn))

    return manager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    devices = initialize_devices()
    lecroy = devices.get("lecroy")
    lecroy.print_id()
