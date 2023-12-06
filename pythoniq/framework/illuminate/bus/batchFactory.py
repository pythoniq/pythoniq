from pythoniq.framework.illuminate.bus.batch import Batch
from pythoniq.framework.illuminate.bus.batchRepository import BatchRepository
from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.queue.factory import Factory as QueueFactory
from pythoniq.framework.illuminate.support.str import Str
import time


class BatchFactory:
    # The queue factory implementation.
    _queue: QueueFactory = None

    # Create a new batch factory instance.
    def __init__(self, queue: QueueFactory):
        self._queue = queue

    def make(self, repository: BatchRepository, id_: str, name: str, totalJobs: int, pendingJobs: int, failedJobs: int,
             options: dict, createdAt: int, cancelledAt: int, finishedAt: int | None):
        return Batch(self._queue, repository, id_, name, totalJobs, pendingJobs, failedJobs, options, createdAt, cancelledAt, finishedAt)

