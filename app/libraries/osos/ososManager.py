from app.libraries.osos.ososContract import OsosContract
from pythoniq.framework.illuminate.support.manager import Manager
from app.libraries.gsm.gsmContract import GsmContract
from app.libraries.gsm.pin import Pin


class OsosManager(Manager, GsmContract):
    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('osos.default', 'gridbox')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('osos.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        return self._config.get('osos.drivers.' + name, {})

    # Drivers
    # Create an instance of the Sha256 hash Driver.
    def createGridboxDriver(self, config: dict) -> OsosContract:
        from app.libraries.osos.gridboxDriver import GridBox

        return GridBox(config)

    # Methods
    def version(self) -> str:
        return self.driver().version()
