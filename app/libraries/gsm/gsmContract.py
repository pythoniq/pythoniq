from app.libraries.gsm.uart import UART
from pythoniq.framework.illuminate.contracts.config.repository import Repository as ConfigContract
from app.libraries.gsm.pin import Pin


class GsmContract:
    def config(self) -> ConfigContract:
        pass

    def pin(self, name: str = None) -> dict | Pin:
        pass

    def on(self) -> None:
        pass

    def off(self) -> None:
        pass

    def restart(self) -> None:
        pass

    def powerOn(self) -> None:
        pass

    def powerOff(self) -> None:
        pass

    def active(self) -> int:
        pass

    def deActive(self) -> None:
        pass

    def uart(self) -> UART:
        pass

    def setIpAddress(self, ip: str) -> None:
        pass
