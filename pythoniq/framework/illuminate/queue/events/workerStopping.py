from pythoniq.framework.illuminate.queue.workerOptions import WorkerOptions


class WorkerStopping:
    # The worker exit status.
    status: int = None

    # The worker instance.
    workerOptions: WorkerOptions = None

    # Create a new event instance.
    def __init__(self, status: int = 0, workerOptions: WorkerOptions = None):
        self.status = status
        self.workerOptions = workerOptions
