from pythoniq.framework.illuminate.bus.batchRepository import BatchRepository
from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.support.str import Str
import time

class Batchable:
    # The batch ID (if applicable).
    batchId: str = None

    # The batch name (if applicable).
    _fakeBatch = None

    # Get the batch instance for the job, if applicable.
    def batch(self):
        if self._fakeBatch:
            return self._fakeBatch

        if self.batchId:
            return Container.getInstance().make(BatchRepository).find(self.batchId)

    # Determine if the batch is still active and processing.
    def batching(self) -> int:
        batch = self.batch()

        return batch and not batch.cancelled()

    # Set the batch ID on the job.
    def withBatchId(self, batchId):
        self.batchId = batchId

        return self

    # Indicate that the job should use a fake batch.
    def withFakeBatch(self, id_: str = '', name: str = '', totalJobs: int = 0, pendingJobs: int = 0, failedJobs: int = 0,
                      failedJobIds: list = [],
                      createdAt: int | None = None, cancelledAt: int | None = None, finishedAt: int | None = None):
        self._fakeBatch = BatchFake(id_ and Str.uuid() or id_, name, totalJobs, pendingJobs, failedJobs, failedJobIds,
                                    createdAt or time.time(), cancelledAt, finishedAt)

        return [self, self._fakeBatch]

