from pythoniq.framework.illuminate.contracts.config.repository import Repository
from pythoniq.framework.illuminate.contracts.foundation.application import Application
from pythoniq.framework.illuminate.support.str import Str


class Manager:
    # The container instance.
    _app: Application = None

    # The configuration repository instance.
    _config: Repository = None

    # The registered custom driver creators.
    _customCreators: dict = {}

    # The array of created "drivers".
    _drivers: dict = {}

    # Create a new manager instance.
    def __init__(self, app: Application):
        self._app = app
        self._config = app.make('config')

    # Get the default driver name.
    def getDefaultDriver(self):
        raise NotImplementedError()

    # Set the default log driver name.
    def setDefaultDriver(self, name: str):
        raise NotImplementedError()

    # Get the configuration.
    def _configurationFor(self, name: str) -> dict:
        raise NotImplementedError()

    # Get a driver instance.
    def driver(self, driver: str = None) -> any:
        driver = driver or self.getDefaultDriver()

        if not driver:
            raise RuntimeError('Unable to resolve NULL driver for [{}]'.format(self.__class__.__name__))

        # If the given driver has not been created before, we will create the instances
        # here and cache it so we can return it next time very quickly. If there is
        # already a driver created by this name, we'll just return that instance.
        if driver not in self._drivers:
            self._drivers[driver] = self._resolve(driver)

        return self._drivers[driver]

    # Resolve the given log instance by name.
    def _resolve(self, name: str, config: dict | None = None):
        if config is None:
            config = self._configurationFor(name)

        if config['driver'] in self._customCreators:
            return self._callCustomCreator(config)

        driverMethod = 'create' + Str().studly(config['driver']) + 'Driver'

        if hasattr(self, driverMethod):
            return getattr(self, driverMethod)(config)

        raise ValueError('Driver [' + name + '] is not supported.')

    # Call a custom driver creator.
    def _callCustomCreator(self, config) -> any:
        return self._customCreators[config['driver']](self._app, config)

    # Register a custom driver creator Closure.
    def extend(self, driver: str, callback: callable):
        self._customCreators[driver] = callback

        return self

    # Get all of the created "drivers".
    def getDrivers(self) -> dict:
        return self._drivers

    # Forget all of the resolved driver instances.
    def forgetDrivers(self):
        self._drivers = {}

        return self

    # Get the container instance used by the manager.
    def getApplication(self) -> Application:
        return self._app

    # Set the container instance used by the manager.
    def setApplication(self, container: Application):
        self._app = container

        return self

    # Dynamically call the default driver instance.
    def __getattr__(self, method):
        def _missing(*args):
            return getattr(self.driver(), method)(*args)

        return _missing
