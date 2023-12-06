from pythoniq.framework.illuminate.contracts.debug.exceptionHandler import ExceptionHandler
from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.queue.queueManager import QueueManager
from pythoniq.framework.illuminate.queue.connectors.nullConnector import NullConnector
from pythoniq.framework.illuminate.queue.connectors.syncConnector import SyncConnector
from pythoniq.framework.illuminate.queue.connectors.arrayConnector import ArrayConnector
from pythoniq.framework.illuminate.queue.worker import Worker
from pythoniq.framework.illuminate.support.facades.facade import Facade
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.support.helpers import tap


class QueueServiceProvider(DeferrableProvider, ServiceProvider):
    def register(self):
        self._registerManager()
        self._registerConnection()
        self._registerWorker()

    # Register the queue manager.
    def _registerManager(self) -> None:
        def fn(app):
            # Once we have an instance of the queue manager, we will register the various
            # resolvers for the queue connectors. These connectors are responsible for
            # creating the classes that accept queue configs and instantiate queues.

            return tap(QueueManager(app), lambda manager: self._registerConnectors(manager))

        self._app.singleton('queue', fn)

    # Register the default queue connection binding.
    def _registerConnection(self):
        self._app.singleton('queue.connection', lambda app: self._app.make('queue').connection())

    # Register the connectors on the queue manager.
    def _registerConnectors(self, manager):
        self._registerNullConnector(manager)

        self._registerSyncConnector(manager)

        self._registerArrayConnector(manager)

    # Register the Null queue connector.
    def _registerNullConnector(self, manager):
        manager.addConnector('null', lambda: NullConnector())

    # Register the Null queue connector.
    def _registerSyncConnector(self, manager):
        manager.addConnector('sync', lambda: SyncConnector())

    # Register the Array queue connector.
    def _registerArrayConnector(self, manager):
        manager.addConnector('array', lambda: ArrayConnector())

    # Register the queue worker.
    def _registerWorker(self):
        def fn(app):
            isDownForMaintenance = lambda: self._app.isDownForMaintenance()

            def resetScope():
                if hasattr(self._app['log'].driver(), 'withoutContext'):
                    self._app['log'].withoutContext()

                self._app['log'].forgetScopedInstances()
                Facade.clearResolvedInstances()

            return Worker(
                app['queue'],
                app['events'],
                app[ExceptionHandler],
                isDownForMaintenance,
                resetScope,
            )

        self._app.singleton('queue.worker', fn)

    # Get the services provided by the provider.
    def provides(self):
        return [
            'queue',
            'queue.connection',
            'queue.failer',
            'queue.listener',
            'queue.worker',
        ]
