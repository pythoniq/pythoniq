from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract


class JobQueued:
    # The connection name.
    connectionName: str = None

    # The job ID.
    id: str | int | None = None

    # The job instance.
    job: callable | str | object = None

    # Create a new event instance.
    def __init__(self, connectionName: str, id_: str | int | None, job: callable | str | object):
        self.connectionName = connectionName
        self.id = id_
        self.job = job
