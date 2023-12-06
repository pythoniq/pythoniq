from pythoniq.framework.illuminate.queue.workerOptions import WorkerOptions


class ListenerOptions(WorkerOptions):
    # The environment the worker should run in.
    environment: str = None

    # Create a new listener options instance.
    def __init__(self, name: str = 'default', environment: str | None = None, backoff: int = 0, memory: int = 128,
                 timeout: int = 60, sleep: int = 3, maxTries: int = 1, force: bool = False, rest: int = 0):
        self.environment = environment

        super().__init__(name, backoff, memory, timeout, sleep, maxTries, force, False, 0, 0, rest)
