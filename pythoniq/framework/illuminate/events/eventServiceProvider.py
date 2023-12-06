from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.events.dispatcher import Dispatcher


class EventServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton('events', lambda app: Dispatcher(app).setQueueResolver(app.make('queue')))
