from pythoniq.framework.illuminate.contracts.cache.lock import Lock


class LockProvider:
    # Get a lock instance.
    def lock(self, name: str, seconds: int = 0, owner: str | None = None) -> Lock:
        pass

    # Restore a lock instance using the owner identifier.
    def restoreLock(self, name: str, owner: str) -> Lock:
        pass
