class JobQueued:
    # The connection name.
    connectionName: str

    # The job ID
    jobId: str | int | None

    # The job payload.
    payload: callable | str | object

    def __init__(self, connectionName: str, id_: str | int | None, job: callable | str | object) -> None:
        self.connectionName = connectionName
        self.id = id_
        self.job = job
