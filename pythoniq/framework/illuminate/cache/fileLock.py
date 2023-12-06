from pythoniq.framework.illuminate.cache.cacheLock import CacheLock


class FileLock(CacheLock):
    # Attempt to acquire the lock.
    def acquire(self):
        return self._store.add(self._name, 1, self._seconds)
