class WorkerOptions:
    # The name of the worker.
    name: str = None

    # The number of seconds to wait before retrying a job that encountered an uncaught exception.
    backoff: int = None

    # The maximum amount of RAM the worker may consume.
    memory: int = None

    # The maximum number of seconds a child worker may run.
    timeout: int = None

    # The number of seconds to wait in between polling the queue.
    sleep: int = None

    # The number of seconds to rest between jobs.
    rest: int = None

    # The maximum number of times a job may be attempted.
    maxTries: int = None

    # Indicates if the worker should run in maintenance mode.
    force: bool = None

    # Indicates if the worker should stop when the queue is empty.
    stopWhenEmpty: bool = None

    # The maximum number of jobs to run.
    maxJobs: int = None

    # The maximum number of seconds a worker may live.
    maxTime: int = None

    # Create a new worker options instance.
    def __init__(self, name: str = 'default', backoff: int = 0, memory: int = 128, timeout: int = 60, sleep: int = 3,
                 maxTries: int = 1, force: bool = False, stopWhenEmpty: bool = False, maxJobs: int = 0,
                 maxTime: int = 0, rest: int = 0):
        self.name = name
        self.backoff = backoff
        self.sleep = sleep
        self.reset = rest
        self.force = force
        self.memory = memory
        self.timeout = timeout
        self.maxTries = maxTries
        self.stopWhenEmpty = stopWhenEmpty
        self.maxJobs = maxJobs
        self.maxTime = maxTime
