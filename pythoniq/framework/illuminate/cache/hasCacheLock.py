from pythoniq.framework.illuminate.cache.lock import Lock
from pythoniq.framework.illuminate.cache.cacheLock import CacheLock


class HasCacheLock:
    # Get a lock instance.
    def lock(self, name: str, seconds: int = 0, owner: str | None = None) -> Lock:
        return CacheLock(self, name, seconds, owner)

    # Restore a lock instance using the owner identifier.
    def restoreLock(self, name: str, owner: str) -> Lock:
        return self.lock(name, 0, owner)
