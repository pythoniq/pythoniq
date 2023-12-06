from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract
from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.queue.jobs.job import Job


class SyncJob(Job, JobContract):
    # The class name of the job.
    _job: str = None

    # The queue message data.
    _payload: str = None

    # Create a new job instance.
    def __init__(self, container: Container, payload: str, connectionName: str, queue=str) -> None:
        self._container = container
        self._payload = payload
        self._connectionName = connectionName
        self._queue = queue

    # Release the job back into the queue after (n) seconds.
    def release(self, delay: int = 0) -> None:
        super().release(delay)

    # Get the number of times the job has been attempted.
    def attempts(self) -> int:
        return 1

    # Get the job identifier.
    def getJobId(self) -> str:
        return ''

    # Get the raw body string for the job.
    def getRawBody(self) -> str:
        return self._payload

    # Get the name of the queue the job belongs to.
    def getQueue(self) -> str:
        return 'sync'
