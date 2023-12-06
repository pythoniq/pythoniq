from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.cache.repository import Repository as CacheContract
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime


class WithoutOverlapping(InteractsWithTime):
    # The job's unique key used for preventing overlaps.
    key: str = None

    # The number of seconds before a job should be available again if no lock was acquired.
    releaseAfter_: int = None

    # The number of seconds before the lock should expire.
    expiresAfter_: int = None

    # The prefix of the lock key.
    prefix: str = 'pythoniq-queue-overlap:'

    # Share the key across different jobs.
    shareKey: bool = False

    # Create a new middleware instance.
    def __init__(self, key='', releaseAfter: int = 0, expiresAfter: int = 0):
        self.key = key
        self.releaseAfter_ = releaseAfter
        self.expiresAfter_ = expiresAfter

    # Process the job.
    def handle(self, job, next):
        lock = Container.getInstance().make(CacheContract).lock(self.getLockKey(job), self.expiresAfter_)

        if lock.get():
            try:
                next(job)
            finally:
                lock.release()
        elif self.releaseAfter_ is not None:
            self.release(self.releaseAfter_)

    # Set the delay (in seconds) to release the job back to the queue.
    def releaseAfter(self, releaseAfter):
        self.releaseAfter_ = releaseAfter

        return self

    # Do not release the job back to the queue if no lock can be acquired.
    def dontRelease(self):
        self.releaseAfter_ = None

        return self

    # Set the maximum number of seconds that can elapse before the lock is released.
    def expiresAfter(self, expiresAfter):
        self.expiresAfter_ = self._secondsUntil(expiresAfter)

        return self

    # Set the prefix of the lock key.
    def withPrefix(self, prefix):
        self.prefix = prefix

        return self

    # Indicate that the lock key should be shared across job classes.
    def shared(self):
        self.shareKey = True

        return self

    # Get the lock key for the given job.
    def getLockKey(self, job):
        return self.shareKey and self.prefix + self.key or self.prefix + job.__class__.__name__ + self.key
