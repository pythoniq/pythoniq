from lib.phpserialize import serialize
from pythoniq.framework.illuminate.collections.arr import Arr


class Queueable:
    # The name of the connection the job should be sent to.
    connection: str | None = None

    # The name of the queue the job should be sent to.
    queue: str | None = None

    # The name of the connection the chain should be sent to.
    chainConnection: str | None = None

    # The name of the queue the chain should be sent to.
    chainQueue: str | None = None

    # The callbacks to be executed on chain failure.
    chainCatchCallbacks: list[callable] = []

    # The number of seconds before the job should be made available.
    _delay: int | None = None

    # Indicates whether the job should be dispatched after all database transactions have committed.
    _afterCommit: bool | None = None

    # The middleware the job should be dispatched through.
    middleware: list[str] = []

    # The jobs that should run if this job is successful.
    chained: list[callable] = []

    # Set the desired connection for the job.
    def onConnection(self, connection: str):
        self.connection = connection

        return self

    # Set the desired queue for the job.
    def onQueue(self, queue: str):
        self.queue = queue

        return self

    # Set the desired connection for the chain.
    def allOnConnection(self, connection: str):
        self.chainConnection = connection
        self.connection = connection

        return self

    # Set the desired queue for the chain.
    def allOnQueue(self, queue: str):
        self.chainQueue = queue
        self.queue = queue

        return self

    # Set the desired delay in seconds for the job.
    def delay(self, delay: int):
        self._delay = delay

        return self

    # Indicate that the job should be dispatched after all database transactions have committed.
    def afterCommit(self):
        self._afterCommit = True

        return self

    # Indicate that the job should not wait until database transactions have been committed before dispatching.
    def beforeCommit(self):
        self._afterCommit = False

        return self

    # Specify the middleware the job should be dispatched through.
    def through(self, middleware: list[str]):
        self.middleware = Arr.wrap(middleware)

        return self

    # Set the jobs that should run if this job is successful.
    def chain(self, chain: list[callable]):
        self.chained = []
        for job in chain:
            self.chained.append(self._serializeJob(job))

        return self

    # Prepend a job to the current chain so that it is run after the currently running job.
    def prependToChain(self, job: list[callable]):
        self.chained = Arr.prepend(self.chained, self._serializeJob(job))

        return self

    # Append a job to the end of the current chain.
    def appendToChain(self, job: list[callable]):
        self.chained = self.chained + [self._serializeJob(job)]

        return self

    # Serialize a job for queuing.
    def _serializeJob(self, job: list[callable]):
        from pythoniq.framework.illuminate.queue.callQueuedClosure import CallQueuedClosure
        if callable(job):
            if issubclass(job, Queueable):
                raise RuntimeError('To enable support for closure jobs, please install the illuminate/queue package.')

            job = CallQueuedClosure.create(job)

        return serialize(job)


    # Dispatch the next job on the chain.
    def dispatchNextJobInChain(self):
        if not self.chained:
            return

    # Invoke all of the chain's failed job callbacks.
    def callChainCatchCallbacks(self, e: Exception):
        for callback in self.chainCatchCallbacks:
            callback(self, e)

