from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.support.str import Str
from lib.helpers import uniqid


class TagSet:
    # The cache store implementation.
    _store: Store = None

    # The tag names.
    _names: list = None

    # Create a new tag set instance.
    def __init__(self, store: Store, names: list):
        self._names = names
        self._store = store

    # Reset all tags in the set.
    def reset(self):
        list(map(lambda name: self.resetTag(name), self._names))

    # Reset the tag and return the new tag identifier.
    def resetTag(self, name: str) -> str:
        id_ = Str.replace('.', ',', uniqid('', True))
        self._store.forever(self.tagKey(name), id_)

        return id_

    # Flush all the tags in the set.
    def flush(self) -> None:
        list(map(lambda name: self.flushTag(name), self._names))

    #  Flush the tag from the cache.
    def flushTag(self, name: str) -> None:
        self._store.delete(self.tagKey(name))

    # Get a unique namespace that changes when any of the tags are flushed.
    def getNamespace(self) -> str:
        return self.tagIds().join('|')

    # Get an array of tag identifiers for all of the tags in the set.
    def tagIds(self) -> list:
        return list(map(lambda name: self.tagId(name), self._names))

    # Get the unique tag identifier for a given tag.
    def tagId(self, name: str) -> str:
        return self._store.get(self.tagKey(name)) or self.resetTag(name)

    # Get the tag identifier key for a given tag.
    def tagKey(self, name: str) -> str:
        return 'tag:' + name + ':key'

    # Get all of the tag names in the set.
    def getNames(self) -> list:
        return self._names
