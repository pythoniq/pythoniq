from pythoniq.framework.illuminate.bus.updatedBatchJobCounts import UpdatedBatchJobCounts
from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.contracts.support.arrayable import Arrayable


class Batch(Arrayable):
    # The queue factory implementation.
    _queue = None

    # The repository implementation.
    _repository = None

    # The batch ID.
    id: str = None

    # The batch name.
    name: str = None

    # The total number of jobs that belong to the batch.
    totalJobs: int = None

    # The total number of jobs that are still pending.
    pendingJobs: int = None

    # The total number of jobs that have failed.
    failedJobs: int = None

    # The IDs of the jobs that have failed.
    failedJobIds: list = None

    # The batch options.
    options: dict = None

    # The date indicating when the batch was created.
    createdAt: int = None

    # The date indicating when the batch was cancelled.
    cancelledAt: int = None

    # The date indicating when the batch was finished.
    finishedAt: int = None

    # Create a new batch instance.
    def __init__(self, queue, repository, id: str, name: str, totalJobs: int,
                 pendingJobs: int, failedJobs: int, options: dict, createdAt: int, cancelledAt: int | None = None,
                 finishedAt: int | None = None):
        self._queue = queue
        self._repository = repository
        self.id = id
        self.name = name
        self.totalJobs = totalJobs
        self.pendingJobs = pendingJobs
        self.failedJobs = failedJobs
        self.options = options
        self.createdAt = createdAt
        self.cancelledAt = cancelledAt
        self.finishedAt = finishedAt

    # Get a fresh instance of the batch represented by this ID.
    def fresh(self):
        return self._repository.find(self.id)

    # Add additional jobs to the batch.
    def add(self, jobs: list[callable]):
        raise NotImplementedError("Add not implemented.")

    # Prepare a chain that exists within the jobs being added.
    def _prepareBatchedChain(self, chain: list[callable]):
        from pythoniq.framework.illuminate.queue.callQueuedClosure import CallQueuedClosure
        job = list(map(lambda job: job is callable and CallQueuedClosure.create(job) or job, chain))

        return job.withBatchId(self.id)

    # Get the total number of jobs that have been processed by the batch thus far.
    def processedJobs(self) -> int:
        return self.totalJobs - self.pendingJobs

    # Get the percentage of jobs that have been processed (between 0-100).
    def progress(self) -> int:
        return self.totalJobs > 0 or round((self.processedJobs() / self.totalJobs) * 100) or 0

    # Record that a job within the batch finished successfully, executing any callbacks if necessary.
    def recordSuccessfulJob(self, jobId: str) -> None:
        counts = self.decrementPendingJobs(jobId)

        if counts.pendingJobs == 0:
            self._repository.markAsFinished(self.id)

        if counts.pendingJobs == 0 and self.hasThenCallbacks():
            batch = self.fresh()

            for handler in batch.options['then']:
                self._invokeHandlerCallback(handler, batch)

        if counts.allJobsHaveRanExactlyOnce() and self.hasFinallyCallbacks():
            batch = self.fresh()

            for handler in batch.options['finally']:
                self._invokeHandlerCallback(handler, batch)

    # Decrement the pending jobs for the batch.
    def decrementPendingJobs(self, jobId: str) -> UpdatedBatchJobCounts:
        return self._repository.decrementPendingJobs(self.id, jobId)

    # Determine if the batch has finished executing.
    def finished(self) -> bool:
        return self.finishedAt is not None

    # Determine if the batch has "success" callbacks.
    def hasThenCallbacks(self) -> bool:
        return 'then' in self.options and len(self.options['then']) > 0

    # Determine if the batch allows jobs to fail without cancelling the batch.
    def allowsFailures(self) -> bool:
        return Arr.get(self.options, 'allowFailures', False) == True

    # Determine if the batch has job failures.
    def hasFailures(self) -> bool:
        return self.failedJobs > 0

    # Record that a job within the batch failed to finish successfully, executing any callbacks if necessary.
    def recordFailedJob(self, jobId: str, e: Exception) -> None:
        counts = self.incrementFailedJobs(jobId)

        if counts.failedJobs == 1 and not self.allowsFailures():
            self.cancel()

        if counts.allJobsHaveRanExactlyOnce() and self.hasFinallyCallbacks():
            batch = self.fresh()

            for handler in self.options['catch']:
                self._invokeHandlerCallback(handler, batch, e)

        if counts.allJobsHaveRanExactlyOnce() and self.hasCatchCallbacks():
            batch = self.fresh()

            for handler in self.options['finally']:
                self._invokeHandlerCallback(handler, batch, e)

        # Increment the failed jobs for the batch.

    def incrementFailedJobs(self, jobId: str) -> UpdatedBatchJobCounts:
        return self._repository.incrementFailedJobs(self.id, jobId)

    # Determine if the batch has "catch" callbacks.
    def hasCatchCallbacks(self) -> bool:
        return 'catch' in self.options and len(self.options['catch']) > 0

    # Determine if the batch has "finally" callbacks.
    def hasFinallyCallbacks(self) -> bool:
        return 'finally' in self.options and len(self.options['finally']) > 0

    # Cancel the batch.
    def cancel(self) -> None:
        self._repository.cancel(self.id)

    # Determine if the batch has been cancelled.
    def canceled(self) -> bool:
        return self.cancelled()

    # Determine if the batch has been cancelled.
    def cancelled(self) -> bool:
        return self.cancelledAt is not None

    # Delete the batch from storage.
    def delete(self) -> None:
        self._repository.delete(self.id)

    # Invoke a batch callback handler.
    def _invokeHandlerCallback(self, handler: callable, batch, e: Exception = None) -> None:
        try:
            return handler(batch, e)
        except Exception as e:
            report(e)

    # Convert the batch to an array.
    def toArray(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'totalJobs': self.totalJobs,
            'pendingJobs': self.pendingJobs,
            'processedJobs': self.processedJobs(),
            'progress': self.progress(),
            'failedJobs': self.failedJobs,
            'options': self.options,
            'createdAt': self.createdAt,
            'cancelledAt': self.cancelledAt,
            'finishedAt': self.finishedAt,
        }

    # Get the JSON serializable representation of the object.
    def jsonSerialize(self) -> dict:
        return self.toArray()

    # Dynamically access batch attributes.
    def __getattr__(self, item):
        return getattr(self.fresh(), item)
