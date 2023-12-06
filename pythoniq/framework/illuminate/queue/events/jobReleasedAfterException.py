from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract


class JobReleasedAfterException:
    # The connection name.
    connectionName: str = None

    # The job instance.
    job: JobContract = None

    # Create a new event instance.
    def __init__(self, connectionName: str, job: JobContract):
        self.job = job
        self.connectionName = connectionName
