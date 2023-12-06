class Job:
    # Get the UUID of the job.
    def uuid(self) -> str | None:
        pass

    # Get the job identifier.
    def getJobId(self) -> str:
        pass

    # Get the decoded body of the job.
    def payload(self) -> dict:
        pass

    # Fire the job.
    def fire(self) -> None:
        pass

    # Release the job back into the queue after (n) seconds.
    def release(self, delay: int = 0) -> None:
        pass

    # Determine if the job was released back into the queue.
    def isReleased(self) -> bool:
        pass

    # Delete the job from the queue.
    def delete(self) -> None:
        pass

    # Determine if the job has been deleted.
    def isDeleted(self) -> bool:
        pass

    # Determine if the job has been deleted or released.
    def isDeletedOrReleased(self) -> bool:
        pass

    # Get the number of times the job has been attempted.
    def attempts(self) -> int:
        pass

    # Determine if the job has been marked as a failure.
    def hasFailed(self) -> int:
        pass

    # Mark the job as "failed".
    def markAsFailed(self) -> None:
        pass

    # Delete the job, call the "failed" method, and raise the failed job event.
    def fail(self, e=None) -> None:
        pass

    # Get the number of times to attempt a job.
    def maxTries(self) -> int | None:
        pass

    # Get the maximum number of exceptions allowed, regardless of attempts.
    def maxExceptions(self) -> int | None:
        pass

    # Get the number of seconds the job can run.
    def timeout(self) -> int | None:
        pass

    # Get the timestamp indicating when the job should timeout.
    def retryUntil(self) -> int | None:
        pass

    # Get the name of the queued job class.
    def getName(self) -> str:
        pass

    # Get the resolved name of the queued job class.
    # Resolves the name of "wrapped" jobs such as class-based handlers.
    def resolveName(self) -> str:
        pass

    # Get the name of the connection the job belongs to.
    def getConnectionName(self) -> str:
        pass

    # Get the name of the queue the job belongs to.
    def getQueue(self) -> str:
        pass

    # Get the raw body string for the job.
    def getRawBody(self) -> str:
        pass
