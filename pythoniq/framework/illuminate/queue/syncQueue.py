from pythoniq.framework.illuminate.contracts.queue.queue import Queue as QueueContract
from pythoniq.framework.illuminate.queue.queue import Queue
from pythoniq.framework.illuminate.queue.events.jobExceptionOccurred import JobExceptionOccurred
from pythoniq.framework.illuminate.queue.events.jobProcessed import JobProcessed
from pythoniq.framework.illuminate.queue.events.jobProcessing import JobProcessing
from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract
from pythoniq.framework.illuminate.queue.jobs.syncJob import SyncJob


class SyncQueue(Queue, QueueContract):
    # Get the size of the queue.
    def size(self, queue: str | None = None) -> int:
        return 0

    # Push a new job onto the queue.
    def push(self, job: str | object, data: any = '', queue: str | None = None) -> any:
        queueJob = self._resolveJob(self._createPayload(job, queue, data), queue)

        try:
            self._raiseBeforeJobEvent(queueJob)

            queueJob.fire()

            self._raiseAfterJobEvent(queueJob)
        except Exception as e:
            self._handleException(queueJob, e)

        return 0

    # Push a raw payload onto the queue.
    def pushRaw(self, payload: str, queue: str | None = None, options: list = []) -> any:
        return None

    # Push a new job onto the queue after (n) seconds.
    def later(self, delay: int, job: str | object, data: any = '', queue=None) -> None:
        self.push(job, data, queue)

    # Pop the next job off of the queue.
    def pop(self, queue: str | None = None) -> JobContract | None:
        return None

    # Resolve a Sync job instance.
    def _resolveJob(self, payload: str, queue: str | None = None) -> SyncJob:
        return SyncJob(self._container, payload, self._connectionName, queue)

    # Raise the before queue job event.
    def _raiseBeforeJobEvent(self, job: JobContract) -> None:
        if self._container.bound('events'):
            self._container.make('events').dispatch(JobProcessing(self._connectionName, job))

    # Raise the after queue job event.
    def _raiseAfterJobEvent(self, job: JobContract) -> None:
        if self._container.bound('events'):
            self._container.make('events').dispatch(JobProcessed(self._connectionName, job))

    # Raise the exception occurred queue job event.
    def _raiseExceptionOccurredJobEvent(self, job: JobContract, e: Exception) -> None:
        if self._container.bound('events'):
            self._container.make('events').dispatch(JobExceptionOccurred(self._connectionName, job, e))

    # Handle an exception that occurred while processing a job.
    def _handleException(self, queueJob: JobContract, e: Exception) -> None:
        self._raiseExceptionOccurredJobEvent(queueJob, e)

        queueJob.fail(e)

        raise e
