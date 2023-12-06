from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract


class Queue:
    # Get the size of the queue.
    def size(self, queue: str | None = None) -> int:
        pass

    # Push a new job onto the queue.
    def push(self, job: str | object, data: any = '', queue: str | None = None) -> any:
        pass

    # Push a new job onto the queue.
    def pushOn(self, queue: str, job: str | object, data: any = '') -> any:
        pass

    # Push a raw payload onto the queue.
    def pushRaw(self, payload: str, queue: str | None = None, options: list = []) -> any:
        pass

    # Push a new job onto the queue after (n) seconds.
    def later(self, delay: int, job: str | object, data: any = '', queue=None):
        pass

    # Push a new job onto a specific queue after (n) seconds.
    def laterOn(self, queue: str, delay: int, job: str | object, data: any = '') -> any:
        pass

    # Push an array of jobs onto the queue.
    def bulk(self, jobs: list, data: any = '', queue: str | None = None):
        pass

    # Pop the next job off of the queue.
    def pop(self, queue: str | None = None) -> JobContract | None:
        pass

    # Get the connection name for the queue.
    def getConnectionName(self) -> str:
        pass

    # Set the connection name for the queue.
    def setConnectionName(self, name: str):
        pass
