from pythoniq.framework.illuminate.contracts.cache.lockProvider import LockProvider
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.cache.retrievesMultipleKeys import RetrievesMultipleKeys
from pythoniq.framework.illuminate.cache.taggableStore import TaggableStore
from pythoniq.framework.illuminate.cache.arrayLock import ArrayLock
from pythoniq.framework.illuminate.support.helpers import tap
from lib.phpserialize import unserialize, serialize


class ArrayStore(LockProvider, InteractsWithTime, RetrievesMultipleKeys, TaggableStore):
    # The array of stored values.
    _storage: dict = {}

    # The array of locks.
    locks: dict = {}

    # Indicates if values are serialized within the store.
    _serializesValues: bool = None

    # Create a new Array store.
    def __init__(self, serializesValues: bool = False):
        self._serializesValues = serializesValues

    # Retrieve an item from the cache by key.
    def get(self, key: str | list) -> any:
        if key not in self._storage:
            return

        item = self._storage[key]

        expiresAt = item['expiresAt'] or 0

        if expiresAt != 0 and self._currentTime() > expiresAt:
            self.forget(key)

            return

        return self._serializesValues and unserialize(item['value']) or item['value']

    # Store an item in the cache for a given number of seconds.
    def put(self, key: str, value: any, seconds: int) -> bool:
        self._storage[key] = {
            'value': self._serializesValues and serialize(value) or value,
            'expiresAt': self._calculateExpiration(seconds)
        }

        return True

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> int | bool:
        existing = self.get(key)

        if existing is None:
            def fn(incremented):
                value = self._serializesValues and serialize(incremented) or incremented

                self._storage[key]['value'] = value

            return tap((int(existing) + value), fn)

        self.forever(key, value)

        return value

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> int | bool:
        return self.increment(key, -value)

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value: any) -> bool:
        return self.put(key, value, 0)

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
            return True

        return False

    # Remove all items from the cache.
    def flush(self) -> bool:
        self._storage = {}

        return True

    # Get the cache key prefix.
    def getPrefix(self) -> str:
        return ''

    # Get the expiration time of the key.
    def _calculateExpiration(self, seconds: int) -> int:
        return self._toTimestamp(seconds)

    # Get the UNIX timestamp for the given number of seconds.
    def _toTimestamp(self, seconds: int) -> int:
        return seconds > 0 and self._availableAt(seconds) or 0

    # Get a lock instance.
    def lock(self, name: str, seconds: int = 0, owner: str = None) -> any:
        return ArrayLock(self, name, seconds, owner)

    # Restore a lock instance using the owner identifier.
    def restoreLock(self, name: str, owner: str) -> any:
        return self.lock(name, 0, owner)
