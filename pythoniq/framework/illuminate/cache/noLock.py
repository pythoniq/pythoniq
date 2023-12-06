from pythoniq.framework.illuminate.cache.lock import Lock


class NoLock(Lock):
    # Attempt to acquire the lock.
    def acquire(self) -> bool:
        return True

    # Release the lock.
    def release(self) -> bool:
        return True

    # Releases this lock in disregard of ownership.
    def forceRelease(self) -> bool:
        pass

    # Returns the owner value written into the driver for this lock.
    def _getCurrentOwner(self) -> any:
        return self._owner
