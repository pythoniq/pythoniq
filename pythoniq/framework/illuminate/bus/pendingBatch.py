from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.bus.batchRepository import BatchRepository
from pythoniq.framework.illuminate.bus.events.batchDispatched import BatchDispatched
from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.events.dispatcher import Dispatcher as EventDispatcher


# @todo: Implement the PendingBatch class.
class PendingBatch:
    # The IoC container instance.
    container: Container = None

    # The batch name.
    name: str = ''

    # The jobs that belong to the batch.
    jobs: list = []

    # The batch options.
    options: dict = {}

    # Create a new pending batch instance.
    def __init__(self, container: Container, jobs: list):
        self.container = container
        self.jobs = jobs

    # Add jobs to the batch.
    def add(self, jobs: iter | object | list):
        jobs = isinstance(jobs, (list, tuple, object)) and jobs or Arr.wrap(jobs)

        for job in jobs:
            self.jobs = [self.jobs, job]

        return self

    # Add a callback to be executed after all jobs in the batch have executed successfully.
    def then(self, callback: callable):
        self.options['then'].append(callback)

        return self

    # Get the "then" callbacks that have been registered with the pending batch.
    def thenCallbacks(self) -> list:
        return self.options['then'] or []

    # Add a callback to be executed after the first failing job in the batch.
    def catch(self, callback: callable):
        self.options['catch'].append(callback)

        return self

    # Get the "catch" callbacks that have been registered with the pending batch.
    def catchCallbacks(self) -> list:
        return self.options['catch'] or []

    # Add a callback to be executed after the batch has finished executing.
    def finally_(self, callback: callable):
        self.options['finally'].append(callback)

        return self

    # Get the "finally" callbacks that have been registered with the pending batch.
    def finallyCallbacks(self) -> list:
        return self.options['finally'] or []

    # Indicate that the batch should not be cancelled when a job within the batch fails.
    def allowFailures(self, allowFailures: bool = True):
        self.options['allowFailures'] = allowFailures

        return self

    # Determine if the pending batch allows jobs to fail without cancelling the batch.
    def allowsFailures(self) -> bool:
        return Arr.get(self.options, 'allowFailures', False) == True

    # Set the name for the batch.
    def name_(self, name: str):
        self.name = name

        return self

    # Specify the queue connection that the batched jobs should run on.
    def onConnection(self, connection: str):
        self.options['connection'] = connection

        return self

    # Get the connection used by the pending batch.
    def connection(self) -> str:
        return self.options['connection'] or None

    # Specify the queue that the batched jobs should run on.
    def onQueue(self, queue: str):
        self.options['queue'] = queue

        return self

    # Get the queue used by the pending batch.
    def queue(self) -> str:
        return self.options['queue'] or None

    # Add additional data into the batch's options array.
    def withOptions(self, key: str, value: any):
        self.options[key] = value

        return self

    # Dispatch the batch.
    def dispatch(self):
        repository = self.container.make(BatchRepository)

        batch = None
        try:
            batch = repository.store(self)

            batch = batch.add(self)
        except Exception as e:
            if batch:
                batch.delete(batch.id)

            raise e

        self.container.make(EventDispatcher).dispatch(BatchDispatched(batch))

        return batch

    # Dispatch the batch after the response is sent to the browser.
    def dispatchAfterResponse(self):
        repository = self.container.make(BatchRepository)

        batch = repository.store(self)

        if batch:
            self.container.terminating(lambda: self.dispatchExistingBatch(batch))

        return batch

    # Dispatch an existing batch.
    def dispatchExistingBatch(self, batch):
        try:
            batch = batch.add(self.jobs)
        except Exception as e:
            batch.delete(batch.id)

            raise e

        self.container.make(EventDispatcher).dispatch(BatchDispatched(batch))

