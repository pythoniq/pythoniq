from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.queue.queueManager import QueueManager
from pythoniq.framework.illuminate.queue.queueServiceProvider import QueueServiceProvider
from pythoniq.framework.illuminate.support.traits.capsuleManagerTrait import CapsuleManagerTrait


class Manager(CapsuleManagerTrait):
    # The queue manager instance.
    _manager: QueueManager = None

    # Create a new queue capsule manager.
    def __init__(self, container: Container = None):
        self._setupContainer(container or Container())

        # Once we have the container setup, we will set up the default configuration
        # options in the container "config" bindings. This'll just make the queue
        # manager behave correctly since all the correct bindings are in place.
        self._setupDefaultConfiguration()

        self._setupManager()

        self._registerConnectors()

    # Setup the default queue configuration options.
    def _setupDefaultConfiguration(self) -> None:
        self._container['config']['queue.default'] = 'default'

    # Build the queue manager instance.
    def _setupManager(self) -> None:
        self._manager = QueueManager(self._container)

    # Register the default connectors that the component ships with.
    def _registerConnectors(self) -> None:
        provider = QueueServiceProvider(self._container)

        provider._registerConnectors(self._manager)

    # Get a connection instance from the global manager.
    @classmethod
    def connection(cls, connection: str = None) -> any:
        return cls._instance.getConnection(connection)

    # Push a new job onto the queue.
    @classmethod
    def push(cls, job: any, data: any = '', queue: str = None, connection: str = None) -> any:
        return cls._instance.connection(connection).pushJob(job, data, queue)

    # Push a new an array of jobs onto the queue.
    @classmethod
    def bulk(cls, jobs: list, data: any = '', queue: str = None, connection: str = None) -> any:
        return cls._instance.connection(connection).bulk(jobs, data, queue)

    # Push a new job onto the queue after (n) seconds.
    @classmethod
    def later(cls, delay: int, job: any, data: any = '', queue: str = None, connection: str = None) -> any:
        return cls._instance.connection(connection).later(delay, job, data, queue)

    # Get a registered connection instance.
    def getConnection(self, name: str = None) -> any:
        return self._manager.connection(name)

    # Register a connection with the manager.
    def addConnection(self, config: dict, name: str = 'default') -> None:
        self._container['config']['queue.connections'][name] = config

    # Get the queue manager instance.
    def getQueueManager(self) -> QueueManager:
        return self._manager

    # Pass dynamic instance methods to the manager.
    def __getattr__(self, method: str) -> any:
        return getattr(self._manager, method)

    # Dynamically pass methods to the default connection.
    def __call__(self, method: str, parameters: list) -> any:
        return getattr(self._manager.connection(), method)(*parameters)
