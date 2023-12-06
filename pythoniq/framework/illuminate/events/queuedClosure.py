class QueuedClosure:
    # The underlying Closure.
    _closure: callable = None

    # The name of the connection the job should be sent to.
    _connection: str | None = None

    # The name of the queue the job should be sent to.
    _queue: str | None = None

    # The number of seconds before the job should be made available.
    _delay: int | None = None

    # All of the "catch" callbacks for the queued closure.
    _catchCallbacks: list = []

    # Create a new queued closure event listener resolver.
    def __init__(self, closure: callable):
        self._closure = closure

    # Set the desired connection for the job.
    def onConnection(self, connection: str | None):
        self._connection = connection

        return self

    # Set the desired queue for the job.
    def onQueue(self, queue: str | None):
        self._queue = queue

        return self

    # Set the desired delay in seconds for the job.
    def delay(self, delay: int | None):
        self._delay = delay

        return self

    # Specify a callback that should be invoked if the queued listener job fails.
    def catch(self, closure: callable):
        self._catchCallbacks.append(closure)

        return self

    # Resolve the actual event listener callback.
    def resolve(self):
        raise NotImplementedError('QueuedClosure')
        def closure(*args):
            return self._closure(*args)
