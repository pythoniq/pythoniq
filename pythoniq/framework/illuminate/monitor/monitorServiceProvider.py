from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.monitor.monitor import Monitor


class MonitorServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton('log', lambda app: Monitor(app))
