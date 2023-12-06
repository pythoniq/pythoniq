from pythoniq.framework.illuminate.contracts.queue.queue import Queue as QueueContract
from pythoniq.framework.illuminate.queue.queue import Queue
from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract


class NullQueue(Queue, QueueContract):
    # Get the size of the queue.
    def size(self, queue: str | None = None) -> int:
        print('pop', queue)
        return 0

    # Push a new job onto the queue.
    def push(self, job: str | object, data: any = '', queue: str | None = None) -> any:
        print('pop', queue, job, data)

    # Push a raw payload onto the queue.
    def pushRaw(self, payload: str, queue: str | None = None, options: list = []) -> any:
        print('pop', queue, payload, options)

    # Push a new job onto the queue after (n) seconds.
    def later(self, delay: int, job: str | object, data: any = '', queue=None):
        print('pop', queue, delay, job, data)

    # Pop the next job off of the queue.
    def pop(self, queue: str | None = None) -> JobContract | None:
        print('pop', queue)
