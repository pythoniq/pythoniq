from pythoniq.framework.illuminate.log.logManager import LogManager
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider


class LogServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton('log', lambda app: LogManager(app))
