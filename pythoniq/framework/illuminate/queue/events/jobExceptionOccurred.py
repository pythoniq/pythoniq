from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract


class JobExceptionOccurred:
    # The connection name.
    connectionName: str = None

    # The job instance.
    job: JobContract = None

    # The exception instance.
    exception: Exception = None

    # Create a new event instance.
    def __init__(self, connectionName: str, job: JobContract, exception: Exception):
        self.job = job
        self.exception = exception
        self.connectionName = connectionName
