from pythoniq.framework.illuminate.bus.queueable import Queueable
from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.contracts.bus.queueingDispatcher import QueueingDispatcher
from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.pipeline.pipeline import Pipeline
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.queue.jobs.syncJob import SyncJob
from pythoniq.framework.illuminate.queue.queue import Queue
import json


class Dispatcher(QueueingDispatcher):
    # Create a new command dispatcher instance.
    def __init__(self, container: Container, queueResolver: callable = None) -> None:
        # The container implementation.
        self._container = container

        # The queue resolver callback.
        self._queueResolver = queueResolver

        # The pipeline instance for the bus.
        self._pipeline = Pipeline(self._container)

        # The pipes to send commands through before dispatching.
        self._pipes: list = []

        # The command to handler mapping for non-self-handling events.
        self._handlers: dict = {}

    # Dispatch a command to its appropriate handler.
    def dispatch(self, command: any) -> any:
        if self._queueResolver and self._commandShouldBeQueued(command):
            return self.dispatchToQueue(command)

        return self.dispatchNow(command)

    # Dispatch a command to its appropriate handler in the current process.
    # Queueable jobs will be dispatched to the "sync" queue.
    def dispatchSync(self, command: any, handler: any = None) -> any:
        if self._queueResolver and self._commandShouldBeQueued(command):
            return self.dispatchToQueue(command)

        return self.dispatchNow(command, handler)

    def dispatchNow(self, command, handler=None):
        uses = command.__class__.__bases__

        if InteractsWithQueue in uses and Queueable in uses and not hasattr(command, 'job'):
            command.setJob(SyncJob(self._container, json.dumps([]), 'sync', 'sync'))

        if handler is None:
            handler = self.getCommandHandler(command)

        if handler:
            def callback(command):
                method = hasattr(handler, 'handle') and 'handle' or '__invoke'

                return getattr(handler, method)(command)
        else:
            def callback(command):
                method = hasattr(command, 'handle') and 'handle' or '__invoke'
                
                return getattr(command, method)(self._container)
                
                return self._container.call([command, method])

        return self._pipeline.send(command).through(self._pipes).then(callback)

    # Create a new chain of queueable jobs.
    def chain(self, jobs: list) -> any:
        jobs = Arr.wrap(jobs)

        return PendingChain

    # Determine if the given command has a handler.
    def hasCommandHandler(self, command: any) -> bool:
        return command in self._handlers

    # Retrieve the handler for a command.
    def getCommandHandler(self, command: any) -> any:
        if self.hasCommandHandler(command):
            return self._container.make(self._handlers[command.__class__])

        return False

    # Determine if the given command should be queued.
    def _commandShouldBeQueued(self, command: any) -> bool:
        return ShouldQueue in command.__class__.__bases__

    # Dispatch a command to its appropriate handler behind a queue.
    def dispatchToQueue(self, command: any) -> any:
        connection = command.connection or None

        queue = getattr(self._queueResolver, connection)

        if issubclass(queue, Queue):
            raise RuntimeError('Queue resolver did not return a Queue implementation.')

        if hasattr(command, 'queue'):
            return command.queue(queue, command)

        return self._pushCommandOnQueue(queue, command)

    # Push the command onto the given queue instance.
    def _pushCommandOnQueue(self, queue: any, command: any) -> any:
        if hasattr(command, 'queue') and hasattr(command, 'delay'):
            return queue.laterOn(command.queue, command.delay, command)

        if hasattr(command, 'queue'):
            return queue.pushOn(command.queue, command)

        if hasattr(command, 'delay'):
            return queue.later(command.delay, command)

        return queue.push(command)

    # Dispatch a command to its appropriate handler after the current process.
    def dispatchAfterResponse(self, command: any, handler: any = None) -> None:
        self._container.terminating(lambda: self.dispatchSync(command, handler))

    # Set the pipes through which commands should be piped before dispatching.
    def pipeThrough(self, pipes: list):
        self._pipes = pipes

        return self

    # Map a command to a handler.
    def map(self, map: dict):
        self._handlers.update(map)

        return self
