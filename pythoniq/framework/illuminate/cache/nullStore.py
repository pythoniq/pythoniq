from pythoniq.framework.illuminate.contracts.cache.lockProvider import LockProvider
from pythoniq.framework.illuminate.cache.taggableStore import TaggableStore
from pythoniq.framework.illuminate.cache.retrievesMultipleKeys import RetrievesMultipleKeys
from pythoniq.framework.illuminate.cache.noLock import NoLock


class NullStore(LockProvider, TaggableStore, RetrievesMultipleKeys):
    # Retrieve an item from the cache by key.
    def get(self, key: str):
        pass

    # Store an item in the cache for a given number of seconds.
    def put(self, key: str, value: any, seconds: int = None) -> bool:
        return False

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> bool:
        return False

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> bool:
        return False

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value: any) -> bool:
        return False

    # Get a lock instance.
    def lock(self, name: str, seconds: int = 0, owner: str = None) -> any:
        return NoLock(name, seconds, owner)

    # Restore a lock instance using the owner identifier.
    def restoreLock(self, name: str, owner: str) -> any:
        return NoLock(name, 0, owner)

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        return True

    # Remove all items from the cache.
    def flush(self) -> bool:
        return True

    # Get the cache key prefix.
    def getPrefix(self) -> str:
        return ''
