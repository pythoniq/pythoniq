from pythoniq.framework.illuminate.contracts.queue.job import Job
from pythoniq.framework.illuminate.queue.manuallyFailedException import ManuallyFailedException
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime


class InteractsWithQueue(InteractsWithTime):
    # The underlying queue job instance.
    _job: Job | None = None

    # Get the number of times the job has been attempted.
    def attempts(self) -> int:
        return self._job and self._job.attempts() or 1

    # Delete the job from the queue.
    def delete(self) -> None:
        if self._job:
            self._job.delete()

    # Fail the job from the queue.
    def fail(self, exception: Exception | None = None) -> None:
        if isinstance(exception, str):
            exception = ManuallyFailedException(exception)

        if isinstance(exception, Exception) or exception is None:
            if self._job:
                return self._job.fail(exception)

        raise TypeError('The fail method requires a string or an instance of Throwable.')

    # Release the job back into the queue after (n) seconds.
    def release(self, delay: int = 0) -> None:
        delay = self.secondsUntil(delay)

        if self._job:
            return self._job.release(delay)

    # Set the base queue job instance.
    def setJob(self, job: Job):
        self._job = job

        return self
