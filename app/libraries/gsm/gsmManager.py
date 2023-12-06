from pythoniq.framework.illuminate.support.manager import Manager
from app.libraries.gsm.gsmContract import GsmContract
from app.libraries.gsm.pin import Pin


class GsmManager(Manager, GsmContract):
    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('gsm.default', 'simcom')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('gsm.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        return self._config.get('gsm.drivers.' + name, {})

    # Drivers
    # Create an instance of the Sha256 hash Driver.
    def createSimcomDriver(self, config: dict) -> GsmContract:
        from app.libraries.gsm.simcomDriver import SimcomDriver

        return SimcomDriver(config)

    # Methods
    def on(self) -> None:
        self.driver().on()

    def off(self) -> None:
        self.driver().off()

    # Get information about the given hashed value.
    def uart(self) -> dict:
        return self.driver().uart()

    def pin(self, name: str = None) -> Pin:
        return self.driver().pin(name)

    def powerOn(self) -> None:
        return self.driver().powerOn()

    def powerOff(self) -> None:
        return self.driver().powerOff()

    def active(self) -> int:
        return self.driver().active()

    def deActive(self) -> None:
        return self.driver().deActive()
