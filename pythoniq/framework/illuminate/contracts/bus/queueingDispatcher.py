from pythoniq.framework.illuminate.contracts.bus.dispatcher import Dispatcher
from pythoniq.framework.illuminate.bus.batch import Batch
from pythoniq.framework.illuminate.bus.pendingBatch import PendingBatch


class QueueingDispatcher(Dispatcher):
    # Attempt to find the batch with the given ID.
    def findBatch(self, id_: str) -> Batch | None:
        pass

    # Create a new batch of queueable jobs.
    def batch(self) -> PendingBatch:
        pass

    # Dispatch a command to its appropriate handler behind a queue.
    def dispatchToQueue(self, command: any) -> any:
        pass
