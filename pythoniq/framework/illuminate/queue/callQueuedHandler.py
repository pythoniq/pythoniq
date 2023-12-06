from pythoniq.framework.illuminate.bus.batchable import Batchable
from pythoniq.framework.illuminate.bus.uniqueLock import UniqueLock
from pythoniq.framework.illuminate.contracts.bus.dispatcher import Dispatcher
from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract
from pythoniq.framework.illuminate.contracts.queue.shouldBeUniqueUntilProcessing import ShouldBeUniqueUntilProcessing
from pythoniq.framework.illuminate.pipeline.pipeline import Pipeline
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.support.facades.app import App


class CallQueuedHandler:
    # The bus dispatcher implementation.
    _dispatcher: Dispatcher = None

    # The container instance.
    _container: Container = None

    # Create a new handler instance.
    def __init__(self, dispatcher: Dispatcher, container: Container = None):
        self._dispatcher = dispatcher
        self._container = container

    # Handle the queued job.
    def call2(self, job: JobContract, data: dict) -> None:
        event = data['command'].data
        listener = data['command'].cls
        
        return listener.handle(*event)

    # Handle the queued job.
    def call(self, job: JobContract, data: dict) -> None:
        command = self._setJobInstanceIfNecessary(job, self._getCommand(data))

        if ShouldBeUniqueUntilProcessing in command.__class__.__bases__:
            self._ensureUniqueJobLockIsReleased(command)

        self._dispatchThroughMiddleware(job, command)

        if not job.isReleased() and not ShouldBeUniqueUntilProcessing in command.__class__.__bases__:
            self._ensureUniqueJobLockIsReleased(command)

        if not job.hasFailed() and not job.isReleased():
            self._ensureNextJobInChainIsDispatched(command)
            self._ensureSuccessfulBatchJobIsRecorded(command)

        if not job.isDeletedOrReleased():
            job.delete()

    # Get the command from the given payload.
    def _getCommand(self, data: dict) -> any:
        return data['command']

    # Dispatch the given job / command through its specified middleware.
    def _dispatchThroughMiddleware(self, job: JobContract, command: any) -> any:
        middleware = []
        if hasattr(command, 'getMiddleware'):
            middleware += command.getMiddleware()

        if hasattr(command, 'middleware'):
            middleware += command.middleware

            return Pipeline(self._container).send(command) \
                .through(middleware) \
                .then(lambda command: self._dispatcher.dispatchNow(command, self._resolveHandler(job, command)))

    # Resolve the handler for the given command.
    def _resolveHandler(self, job: JobContract, command: any) -> any:
        handler = self._dispatcher.getCommandHandler(command) or None

        if handler:
            self._setJobInstanceIfNecessary(job, handler)

        return handler

    # Set the job instance of the given class if necessary.
    def _setJobInstanceIfNecessary(self, job: JobContract, instance: any) -> any:
        if isinstance(instance, InteractsWithQueue):
            instance.setJob(job)

        return instance

    # Ensure the next job in the chain is dispatched if applicable.
    def _ensureNextJobInChainIsDispatched(self, command: any) -> None:
        if hasattr(command, 'dispatchNextJobInChain'):
            command.dispatchNextJobInChain()

    # Ensure the batch is notified of the successful job completion.
    def _ensureSuccessfulBatchJobIsRecorded(self, command: any) -> None:
        if Batchable not in command.__class__.__bases__ or ShouldBeUniqueUntilProcessing not in command.__class__.__bases__:
            return

        batch = command.batch()
        if batch:
            batch.recordSuccessfulJob(command.job.uuid())

    # Ensure the lock for a unique job is released.
    def _ensureUniqueJobLockIsReleased(self, command: any) -> None:
        if not isinstance(command, ShouldBeUniqueUntilProcessing):
            # UniqueLock(App().make('cache')).release(command)
            pass

    # Handle a model not found exception.
    def _handleModelNotFound(self, job: JobContract, e: Exception) -> None:
        cls = job.resolveName()

        job.delete()

        return

    # Call the failed method on the job instance.
    # The event instance and the exception will be passed.
    def failed(self, data: dict, e: Exception, uuid: str) -> None:
        command = self._getCommand(data)

        if ShouldBeUniqueUntilProcessing not in command.__class__.__bases__:
            self._ensureUniqueJobLockIsReleased(command)

        self._ensureBatchIsNotifiedOfFailedJob(uuid, command, e)
        self._ensureChainCatchCallbacksAreInvoked(uuid, command, e)

        if hasattr(command, 'failed'):
            command.failed(e)

    # Ensure the batch is notified of the failed job.
    def _ensureBatchIsNotifiedOfFailedJob(self, uuid: str, command: any, e: Exception) -> None:
        if Batchable not in command.__class__.__bases__:
            return

        batch = command.batch()
        if batch:
            batch.recordFailedJob(uuid, e)

    # Ensure the chained job catch callbacks are invoked.
    def _ensureChainCatchCallbacksAreInvoked(self, uuid: str, command: any, e: Exception) -> None:
        if hasattr(command, 'invokeChainCatchCallbacks'):
            command.invokeChainCatchCallbacks(e)
