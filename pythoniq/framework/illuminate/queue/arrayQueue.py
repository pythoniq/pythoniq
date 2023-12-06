from pythoniq.framework.illuminate.contracts.queue.queue import Queue as QueueContract
from pythoniq.framework.illuminate.queue.queue import Queue
from pythoniq.framework.illuminate.queue.events.jobExceptionOccurred import JobExceptionOccurred
from pythoniq.framework.illuminate.queue.events.jobProcessed import JobProcessed
from pythoniq.framework.illuminate.queue.events.jobProcessing import JobProcessing
from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract
from pythoniq.framework.illuminate.queue.jobs.arrayJob import ArrayJob


class ArrayQueue(Queue, QueueContract):
    _queues: dict = {}
    _queuePointer: int = 0

    # Get the size of the queue.
    def size(self, queue: str | None = None) -> int:
        i = 0
        for queue in self._queues:
            i += len(self._queues[queue])

        return i

    def getQueue(self, queue: str | None = None) -> list:
        if queue is None:
            queue = 'default'

        if queue not in self._queues:
            self._queues[queue] = []

        return self._queues[queue]

    # Push a new job onto the queue.
    def push(self, job: str | object, data: any = '', queue: str | None = 'default') -> any:
        self.getQueue(queue).append(self._resolveJob(self._createPayload(job, queue, data), queue))

    # Push a raw payload onto the queue.
    def pushRaw(self, payload: str, queue: str | None = None, options: list = []) -> any:
        print('pushRaw', queue, payload, options)

    # Push a new job onto the queue after (n) seconds.
    def later(self, delay: int, job: str | object, data: any = '', queue=None):
        print('later', queue, delay, job, data)

    def _nextQueueName(self) -> str:
        return list(self._queues.keys())[self._queuePointer]

    def getJob(self, queueName: str) -> JobContract | None:
        queue = self.getQueue(queueName)
        jobCount = len(queue)
        if jobCount > 0:
            if jobCount == 1:
                self._queues.pop(queueName)
            return queue.pop(0)

        return None

    def findNextJob(self) -> JobContract | None:
        if self._queuePointer >= len(self._queues):
            self._queuePointer = 0

        job = self.getJob(self._nextQueueName())

        self._queuePointer += 1

        return job

    # Pop the next job off of the queue.
    def pop(self, queueName: str | None = None) -> JobContract | None:
        if len(self._queues) == 0:
            return None

        if queueName is not None:
            job = self.getJob(queueName)
        elif len(self._queues) == 1:
            queueName = list(self._queues.keys())[0]
            job = self.getJob(queueName)
        else:
            job = self.findNextJob()

        if job is None:
            return None

        self._raiseBeforeJobEvent(job)

        job.fire()

        self._raiseAfterJobEvent(job)

    # Resolve a Sync job instance.
    def _resolveJob(self, payload: str, queue: str | None = None) -> ArrayJob:
        return ArrayJob(self._container, payload, self._connectionName, queue)

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
    def _handleJobException(self, queueJob: JobContract, e: Exception) -> None:
        self._raiseExceptionOccurredJobEvent(queueJob, e)

        queueJob.fail(e)

        raise e
