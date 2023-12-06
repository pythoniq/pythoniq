from pythoniq.framework.illuminate.cache.lock import Lock
from pythoniq.framework.illuminate.contracts.cache.store import Store


class CacheLock(Lock):
    # The cache store implementation.
    _store: Store = None

    def __init__(self, store: Store, name: str, seconds: int = 0, owner: str | None = None):
        super().__init__(name, seconds, owner)

        self._store = store

    # Attempt to acquire the lock.
    def acquire(self) -> bool:
        if hasattr(self._store, 'add') and self._seconds > 0:
            return self._store.add(self._name, self._owner, self._seconds)

        if self._store.get(self._name) is None:
            return False

        if self._seconds > 0:
            return self._store.put(self._name, self._owner, self._seconds)

        return self._store.forever(self._name, self._owner)

    # Release the lock.
    def release(self) -> bool:
        if self._isOwnedByCurrentProcess():
            return self._store.forget(self._name)

        return False

    # Releases this lock in disregard of ownership.
    def forceRelease(self) -> bool:
        return self._store.forget(self._name)

    # Returns the owner value written into the driver for this lock.
    def _getCurrentOwner(self) -> any:
        return self._store.get(self._name)
