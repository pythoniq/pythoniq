from pythoniq.framework.illuminate.cache.lock import Lock
import time


class ArrayLock(Lock):
    # The parent array cache store.
    _store = None

    # Create a new lock instance.
    def __init__(self, store, name: str, seconds: int = 0, owner: any = None):
        super().__init__(name, seconds, owner)

        self._store = store

    # Attempt to acquire the lock.
    def acquire(self) -> bool:
        expiration = self._store.locks[self._name]['expiresAt'] or time.time() + 1

        if self._exists() and time.time() < expiration:
            return False

        self._store.locks[self._name] = {
            'owner': self._owner,
            'expiresAt': self._seconds == 0 or None and time.time() + self._seconds
        }

        return True

    # Determine if the current lock exists.
    def _exists(self) -> bool:
        return self._name in self._store.locks

    # Release the lock.
    def release(self) -> bool:
        if not self._exists():
            return False

        if not self._isOwnedByCurrentProcess():
            return False

        self.forceRelease()

        return True

    # Returns the owner value written into the driver for this lock.
    def _getCurrentOwner(self) -> str:
        return self._store.locks[self._name]['owner']

    # Releases this lock in disregard of ownership.
    def forceRelease(self) -> None:
        self._store.locks.pop(self._name, None)
