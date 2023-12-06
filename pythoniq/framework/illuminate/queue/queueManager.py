from pythoniq.framework.illuminate.contracts.queue.factory import Factory as FactoryContract
from pythoniq.framework.illuminate.contracts.queue.monitor import Monitor as MonitorContract
from pythoniq.framework.illuminate.contracts.foundation.application import Application
from pythoniq.framework.illuminate.contracts.queue.queue import Queue
from pythoniq.framework.illuminate.queue.events.jobProcessing import JobProcessing
from pythoniq.framework.illuminate.queue.events.jobProcessed import JobProcessed
from pythoniq.framework.illuminate.queue.events.jobExceptionOccurred import JobExceptionOccurred
from pythoniq.framework.illuminate.queue.events.looping import Looping
from pythoniq.framework.illuminate.queue.events.jobFailed import JobFailed
from pythoniq.framework.illuminate.queue.events.workerStopping import WorkerStopping


class QueueManager(FactoryContract, MonitorContract):
    # The application instance.
    _app: Application = None

    # The array of resolved queue connections.
    _connections: dict = {}

    # The array of resolved queue connectors.
    _connectors: dict = {}

    # Create a new queue manager instance.
    def __init__(self, app: Application):
        self._app = app

    # Register an event listener for the before job event.
    def before(self, callback: callable) -> None:
        self._app['events'].listen(JobProcessing, callback)

    # Register an event listener for the after job event.
    def after(self, callback: callable) -> None:
        self._app['events'].listen(JobProcessed, callback)

    # Register an event listener for the exception occurred job event.
    def exceptionOccurred(self, callback: callable) -> None:
        self._app['events'].listen(JobExceptionOccurred, callback)

    # Register an event listener for the daemon queue loop.
    def looping(self, callback: callable) -> None:
        self._app['events'].listen(Looping, callback)

    # Register an event listener for the failed job event.
    def failing(self, callback: callable) -> None:
        self._app['events'].listen(JobFailed, callback)

    # Register an event listener for the daemon queue stopping.
    def stopping(self, callback: callable) -> None:
        self._app['events'].listen(WorkerStopping, callback)

    # Determine if the driver is connected.
    def connected(self, name: str = None) -> bool:
        name = name or self.getDefaultDriver()
        return name in self._connections

    # Resolve a queue connection instance.
    def connection(self, name: str = None) -> Queue:
        name = name or self.getDefaultDriver()

        # If the connection has not been resolved yet we will resolve it now as all
        # of the connections are resolved when they are actually needed so we do
        # not make any unnecessary connection to the various queue end-points.
        if name not in self._connections:
            self._connections[name] = self._resolve(name)

            self._connections[name].setContainer(self._app)

        return self._connections[name]

    # Resolve a queue connection.
    def _resolve(self, name: str = None) -> Queue:
        config = self.getConfig(name)

        if config is None or config == '' or config == 'null':
            raise Exception('The [' + name + '] queue connection has not been configured.')

        return self._getConnector(config['driver']).connect(config).setConnectionName(name)

    # Get the connector for a given driver.
    def _getConnector(self, driver: str) -> callable:
        if driver not in self._connectors:
            raise Exception('No connector for [' + driver + ']')

        return self._connectors[driver]()

    # Add a queue connection resolver.
    def extend(self, driver: str, resolver: callable) -> None:
        self.addConnector(driver, resolver)

    # Add a queue connection resolver.
    def addConnector(self, driver: str, resolver: callable) -> None:
        self._connectors[driver] = resolver

    # Get the queue connection configuration.
    def getConfig(self, name: str) -> dict:
        if name != '' and name != 'null':
            return self._app['config']['queue.connections.' + name]

        return {'driver': 'null'}

    # Get the name of the default queue connection.
    def getDefaultDriver(self) -> str:
        return self._app['config']['queue.default']

    # Set the name of the default queue connection.
    def setDefaultDriver(self, name: str) -> None:
        self._app['config']['queue.default'] = name

    # Get the full name for the given connection.
    def getName(self, connection: str = None) -> str:
        return connection or self.getDefaultDriver()

    # Get the application instance used by the manager.
    def getApplication(self) -> Application:
        return self._app

    # Set the application instance used by the manager.
    def setApplication(self, app: Application):
        self._app = app

        for connection in self._connections.values():
            connection.setContainer(app)

        return self

    # Dynamically pass calls to the default connection.
    def __getattr__(self, method):
        def _missing(*args):
            return getattr(self.connection(), method)(*args)

        return _missing
