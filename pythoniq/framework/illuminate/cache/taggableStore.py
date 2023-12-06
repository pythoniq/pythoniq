from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.cache.taggedCache import TaggedCache
from pythoniq.framework.illuminate.cache.tagSet import TagSet


class TaggableStore(Store):
    # Begin executing a new tags operation.
    def tags(self, *names: list) -> TaggedCache:
        return TaggedCache(self, TagSet(self, list(names)))
