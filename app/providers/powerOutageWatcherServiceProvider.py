from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from app.services.powerOutageWatcherService import PowerOutageWatcherService


class PowerOutageWatcherServiceProvider(ServiceProvider):
    def boot(self):
        cycle = self._app.config().get('hardware.powerOutageWatcher.cycle')
        control = self._app.config().get('hardware.powerOutageWatcher.control')

        watcher = PowerOutageWatcherService(cycle, control)

        self._app.instance('powerOutageWatcherService', watcher)
