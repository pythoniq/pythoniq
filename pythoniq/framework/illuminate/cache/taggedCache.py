from pythoniq.framework.illuminate.cache.repository import Repository
from pythoniq.framework.illuminate.cache.retrievesMultipleKeys import RetrievesMultipleKeys
from pythoniq.framework.illuminate.cache.tagSet import TagSet
from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.cache.events.cacheEvent import CacheEvent
from pythoniq.framework.illuminate.support.facades.app import App


class TaggedCache(Repository, RetrievesMultipleKeys):
    # The tag set instance.
    _tags: TagSet = None

    # Create a new tagged cache instance.
    def __init__(self, store: Store, tags: TagSet):
        super().__init__(store)

        self._tags = tags

    # Store multiple items in the cache for a given number of seconds.
    def putMany(self, values: dict, ttl: int = None) -> bool:
        if ttl is None:
            return self._putManyForever(values)

        return self.putManyAlias(values, ttl)

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: any = 1) -> int:
        return self._store.increment(self._itemKey(key), value)

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: any = 1) -> int:
        return self._store.decrement(self._itemKey(key), value)

    # Remove all items from the cache.
    def flush(self) -> bool:
        self._tags.reset()

        return True

    #
    def _itemKey(self, key: str) -> str:
        return self._taggedItemKey(key)

    # Get a fully qualified key for a tagged item.
    def _taggedItemKey(self, key: str) -> str:
        return App().hash().driver('sha1').make(self._tags.getNamespace() + ':' + key)

    # Fire an event for this cache instance.
    def _event(self, event: CacheEvent) -> None:
        super()._event(event.setTags(self._tags.getNames()))

    # Get the tag set instance.
    def getTags(self) -> TagSet:
        return self._tags

    # Store multiple items in the cache for a given number of seconds.
    def putManyAlias(self, values: dict, ttl: int) -> bool:
        return super().putMany(values, ttl)
