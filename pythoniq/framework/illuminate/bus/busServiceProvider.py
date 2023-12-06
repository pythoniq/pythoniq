from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.bus.dispatcher import Dispatcher
from pythoniq.framework.illuminate.contracts.queue.factory import Factory as QueueFactoryContract
from pythoniq.framework.illuminate.contracts.bus.dispatcher import Dispatcher as DispatcherContract
from pythoniq.framework.illuminate.contracts.bus.queueingDispatcher import \
    QueueingDispatcher as QueueingDispatcherContract
from pythoniq.framework.illuminate.bus.batchRepository import BatchRepository


class BusServiceProvider(DeferrableProvider, ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        def fn(app):
            return Dispatcher(app, lambda app: app[QueueFactoryContract].connection(None))

        self._app.singleton('bus', fn)

        self._app.alias(Dispatcher, DispatcherContract)
        self._app.alias(Dispatcher, QueueingDispatcherContract)

    # Get the services provided by the provider.
    def provides(self) -> list:
        return [
            Dispatcher,
            DispatcherContract,
            QueueingDispatcherContract,
            BatchRepository,
        ]

