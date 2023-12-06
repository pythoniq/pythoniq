from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.battery.battery import Battery


class BatteryServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton('battery', lambda app: Battery(app))
