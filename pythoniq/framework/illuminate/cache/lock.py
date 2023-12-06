from pythoniq.framework.illuminate.contracts.cache.lock import Lock as LockContract
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.contracts.cache.lockTimeoutException import LockTimeoutException
from pythoniq.framework.illuminate.support.sleep import Sleep
from pythoniq.framework.illuminate.support.str import Str


class Lock(LockContract, InteractsWithTime):
    # The name of the lock.
    _name: str = None

    # The number of seconds the lock should be maintained.
    _seconds: int = None

    # The scope identifier of this lock.
    _owner: str = None

    # The number of milliseconds to wait before re-attempting to acquire a lock while blocking.
    _sleepMilliseconds: int = 250

    # Create a new lock instance.
    def __init__(self, name: str, seconds: int, owner: str = None):
        if owner is None:
            owner = Str.random(40)

        self._name = name
        self._owner = owner
        self._seconds = seconds

    # Attempt to acquire the lock.
    def acquire(self) -> bool:
        raise NotImplementedError

    # Release the lock.
    def release(self) -> bool:
        raise NotImplementedError

    # Returns the owner value written into the driver for this lock.
    def getCurrentOwner(self) -> str:
        raise NotImplementedError

    # Attempt to acquire the lock.
    def get(self, callback: callable = None) -> bool:
        result = self.acquire()

        if result and callable(callback):
            try:
                return callback()
            finally:
                self.release()

        return result

    # Attempt to acquire the lock for the given number of seconds.
    def block(self, seconds: int, callback: callable = None) -> bool:
        starting = self._currentTime()

        while not self.acquire():
            Sleep.usleep(self._sleepMilliseconds * 1000)

            if self._currentTime() - seconds >= starting:
                raise LockTimeoutException

        if callable(callback):
            try:
                return callback()
            finally:
                self.release()

        return True

    # Returns the current owner of the lock.
    def owner(self) -> str:
        return self._owner

    # Determines whether this lock is allowed to release the lock in the driver.
    def _isOwnedByCurrentProcess(self) -> bool:
        return self.getCurrentOwner() == self._owner

    # Specify the number of milliseconds to sleep in between blocked lock acquisition attempts.
    def betweenBlockedAttemptsSleepFor(self, milliseconds: int):
        self._sleepMilliseconds = milliseconds

        return self
