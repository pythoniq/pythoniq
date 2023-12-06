from pythoniq.framework.illuminate.queue.queue import Queue


class Factory:
    # Resolve a queue connection instance.
    def connection(self, name: str = None) -> Queue:
        pass
