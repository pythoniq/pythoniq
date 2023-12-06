from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.queue.callQueuedHandler import CallQueuedHandler
from pythoniq.framework.illuminate.queue.events.jobFailed import JobFailed
from pythoniq.framework.illuminate.queue.jobs.jobName import JobName
from pythoniq.framework.illuminate.queue.manuallyFailedException import ManuallyFailedException
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime


class Job(InteractsWithTime):
    # The job handler instance.
    _instance: any = None

    # The IoC container instance.
    _container: Container = None

    # Indicates if the job has been deleted.
    _deleted: bool = False

    # Indicates if the job has been released.
    _released: bool = False

    # Indicates if the job has failed.
    _failed: bool = False

    # The name of the connection the job belongs to.
    _connectionName: str = None

    # The name of the queue the job belongs to.
    _queue: str = None

    # Get the job identifier.
    def getJobId(self) -> str:
        pass

    # Get the UUID of the job.
    def uuid(self) -> str | None:
        return self.payload()['uuid'] or None

    # Fire the job.
    def fire(self) -> None:
        payload = self.payload()
        
        [cls, method] = JobName.parse(payload['job'])

        self._instance = getattr(self._resolve(cls), method)(self, payload['data'])

    # Delete the job from the queue.
    def delete(self) -> None:
        self._deleted = True

    # Determine if the job has been deleted.
    def isDeleted(self) -> bool:
        return self._deleted

    # Release the job back into the queue after (n) seconds.
    def release(self, delay: int = 0) -> None:
        self._released = True

    # Determine if the job was released back into the queue.
    def isReleased(self) -> bool:
        return self._released

    # Determine if the job has been deleted or released.
    def isDeletedOrReleased(self) -> bool:
        return self.isDeleted() or self.isReleased()

    # Determine if the job has been marked as a failure.
    def hasFailed(self) -> bool:
        return self._failed

    # Mark the job as "failed".
    def markAsFailed(self) -> None:
        self._failed = True

    # Delete the job, call the "failed" method, and raise the failed job event.
    def fail(self, e: Exception) -> None:
        self.markAsFailed()

        if self.isDeleted():
            return

        try:
            # If the job has failed, we will delete it, call the "failed" method and then call
            # an event indicating the job has failed so it can be logged if needed. This is
            # to allow every developer to better keep monitor of their failed queue jobs.
            self.delete()

            self.failed(e)
        finally:
            self._resolve('events').dispatch(JobFailed(self._connectionName, self, e or ManuallyFailedException()))

    # Process an exception that caused the job to fail.
    def failed(self, e: Exception) -> None:
        payload = self.payload()

        [cls, method] = JobName.parse(payload['job'])

        self._instance = self._resolve(cls)
        if hasattr(self._instance, 'failed'):
            self._instance.failed(payload['data'], e, payload['uuid'] or '')

    # Resolve the given class.
    def _resolve(self, cls: str) -> any:
        if cls == 'Illuminate\\Queue\\CallQueuedHandler':
            return CallQueuedHandler(self._container.make('bus'), self._container)

        return self._container.make(cls)

    # Get the decoded body of the job.
    def payload(self) -> dict:
        return self.getRawBody()

    # Get the number of times to attempt a job.
    def maxTries(self) -> int:
        return self.payload()['maxTries'] or None

    # Get the number of times to attempt a job after an exception.
    def maxExceptions(self) -> int:
        return self.payload()['maxExceptions'] or None

    # Determine if the job should fail when it timeouts.
    def shouldFailOnTimeout(self) -> bool:
        return self.payload()['failOnTimeout'] or False

    # The number of seconds to wait before retrying a job that encountered an uncaught exception.
    def backoff(self) -> int | list[int] | None:
        return self.payload()['backoff'] or self.payload()['delay'] or None

    # Get the number of seconds the job can run.
    def timeout(self) -> int | None:
        return self.payload()['timeout'] or None

    # Get the timestamp indicating when the job should timeout.
    def retryUntil(self) -> int | None:
        return self.payload()['retryUntil'] or None

    # Get the name of the queued job class.
    def getName(self) -> str:
        return self.payload()['job']

    # Get the resolved name of the queued job class.
    # Resolves the name of "wrapped" jobs such as class-based handlers.
    def resolveName(self) -> str:
        return JobName.resolve(self.getName(), self.payload())

    # Get the name of the connection the job belongs to.
    def getConnectionName(self) -> str:
        return self._connectionName

    # Get the name of the queue the job belongs to.
    def getQueue(self) -> str:
        return self._queue

    # Get the service container instance.
    def getContainer(self) -> Container:
        return self._container
