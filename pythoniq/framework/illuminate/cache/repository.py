from pythoniq.framework.illuminate.contracts.cache.repository import Repository as CacheContract
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.support.traits.macroable import Macroable
from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher
from pythoniq.framework.illuminate.cache.events.cacheHit import CacheHit
from pythoniq.framework.illuminate.cache.events.cacheMissed import CacheMissed
from pythoniq.framework.illuminate.cache.events.keyForgotten import KeyForgotten
from pythoniq.framework.illuminate.cache.events.keyWritten import KeyWritten
from pythoniq.framework.illuminate.collections.helpers import value
from pythoniq.framework.illuminate.support.helpers import tap
import time


class Repository(CacheContract, InteractsWithTime, Macroable):
    # The cache store implementation.
    _store: Store = None

    # The event dispatcher implementation.
    _events: Dispatcher = None

    # The default number of seconds to store items.
    _default: int = 3600

    # Create a new cache repository instance.
    def __init__(self, store: Store):
        self._store = store

    # Handle a result for the "many" method.
    def _handleManyResult(self, keys: list, key: str, value_: any) -> any:
        # If we could not find the cache value, we will fire the missed event and get
        # the default value for this cache value. This default could be a callback
        # so we will execute the value function which will resolve it if needed.
        if value_ is None:
            self._event(CacheMissed(key))

            return key in keys and value(keys[key]) or None

        # If we found a valid value we will fire the "hit" event and return the value
        # back from this function. The "hit" event gives developers an opportunity
        # to listen for every possible cache "hit" throughout this applications.
        self._event(CacheHit(key, value_))

        return value_

    # Store multiple items in the cache indefinitely.
    def _putManyForever(self, values: dict) -> bool:
        result = True

        for key, value in values.items():
            if not self.forever(key, value):
                result = False

        return result

    # Format the key for a cache item.
    def _itemKey(self, key: str) -> str:
        return key

    # Calculate the number of seconds for the given TTL.
    def _getSeconds(self, ttl: int) -> int:
        duration = self._parseDateInterval(ttl)

        duration -= time.time()

        return duration > 0 and duration or 0

    # Determine if the current store supports tags.
    def supportsTags(self) -> bool:
        return hasattr(self._store, 'tags')

    # Get the default cache time.
    def getDefaultCacheTime(self) -> int:
        return self._default

    # Set the default cache time in seconds.
    def setDefaultCacheTime(self, seconds: int) -> 'Repository':
        self._default = seconds

        return self

    # Get the cache store implementation.
    def getStore(self) -> Store:
        return self._store

    # Set the cache store implementation.
    def setStore(self, store: Store) -> 'Repository':
        self._store = store

        return self

    # Fire an event for this cache instance.
    def _event(self, event: any) -> None:
        self._events and self._events.dispatch(event)

    # Get the event dispatcher instance.
    def getEventDispatcher(self) -> Dispatcher:
        return self._events

    # Set the event dispatcher instance.
    def setEventDispatcher(self, events: Dispatcher) -> 'Repository':
        self._events = events

        return self

    # Determine if a given offset exists.
    def offsetExists(self, key: str) -> bool:
        return self.has(key)

    # Get the value at a given offset.
    def offsetGet(self, key: str) -> any:
        return self.get(key)

    # Set the value at a given offset.
    def offsetSet(self, key: str, value: any) -> None:
        self.set(key, value)

    # Unset the value at a given offset.
    def offsetUnset(self, key: str) -> None:
        self.set(key, None)

    def __getitem__(self, key) -> any:
        return self.offsetGet(key)

    def __setitem__(self, key, value) -> None:
        self.offsetSet(key, value)

    def __delitem__(self, key) -> None:
        self.offsetUnset(key)

    # Dynamically access container services.
    def __get__(self, key: str) -> any:
        return self[key]

    # Dynamically set container services.
    def __set__(self, key: str, value: any) -> any:
        self[key] = value

    # Handle dynamic calls into macros or pass missing methods to the store.
    def macroCall(self, method: str, parameters: list) -> any:
        return super.__call__(method, parameters)

    # Handle dynamic calls into macros or pass missing methods to the store.
    def __call__(self, method: str, parameters: list) -> any:
        if self.hasMacro(method):
            return self.macroCall(method, parameters)

        return getattr(self._store, method)(*parameters)

    # Clone cache repository instance.
    def __clone__(self):
        return self.__class__(self._store)

    # Methods

    # Store an item in the cache if the key does not exist.
    def add(self, key: str, value_: any, ttl: int = None) -> bool:
        seconds = None

        if ttl is not None:
            seconds = self._getSeconds(ttl)

            if seconds <= 0:
                return False

            # If the store has an "add" method we will call the method on the store so it
            # has a chance to override this logic. Some drivers better support the way
            # this operation should work with a total "atomic" implementation of it.
            if hasattr(self._store, 'add'):
                return self._store.add(self._itemKey(key), value_, seconds)

        # If the value did not exist in the cache, we will put the value in the cache
        # so it exists for subsequent requests. Then, we will return true so it is
        # easy to know if the value gets added. Otherwise, we will return false.
        if not self.get(key):
            return self.put(key, value_, seconds)

        return False

    # Store an item in the cache.
    def put(self, key: str, value_: any, ttl: int = None) -> bool:
        if isinstance(key, dict):
            return self.putMany(key, value_)

        if ttl is None:
            return self.forever(key, value_)

        seconds = self._getSeconds(ttl)

        if seconds <= 0:
            return self.forget(key)

        result = self._store.put(self._itemKey(key), value_, seconds)

        if result:
            self._event(KeyWritten(key, value_, seconds))

        return result

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value_: any) -> bool:
        result = self._store.forever(self._itemKey(key), value_)

        if result:
            self._event(KeyWritten(key, value_, None))

        return result

    # Retrieve an item from the cache by key.
    def get(self, key: str, default: any = None) -> any:
        if isinstance(key, list):
            return self.many(key)

        value_ = self._store.get(self._itemKey(key))

        # If we could not find the cache value, we will fire the missed event and get
        # the default value for this cache value. This default could be a callback
        # so we will execute the value function which will resolve it if needed.
        if value_ is None:
            self._event(CacheMissed(key))

            value_ = value(default)
        else:
            self._event(CacheHit(key, value_))

        return value_

    # Determine if an item exists in the cache.
    def has(self, key: str) -> bool:
        return self.get(key) is not None

    # Determine if an item doesn't exist in the cache.
    def missing(self, key: str) -> bool:
        return not self.has(key)

    # Retrieve multiple items from the cache by key.
    # Items not found in the cache will have a null value.
    def many(self, keys: list) -> dict:
        values = self._store.many([self._itemKey(key) for key in keys])

    # Store multiple items in the cache for a given number of seconds.
    def putMany(self, values: dict, ttl: int = None) -> bool:
        if ttl is None:
            return self._putManyForever(values)

        seconds = self._getSeconds(ttl)

        if seconds <= 0:
            return self.deleteMultiple(values.keys())

        result = self._store.putMany(values, seconds)

        if result:
            for key in values:
                self._event(KeyWritten(key, values[key], seconds))

        return result

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> int:
        return self._store.increment(key, value)

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> int:
        return self._store.decrement(key, value)

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        return tap(self._store.forget(self._itemKey(key)), lambda result: self._event(KeyForgotten(key)))

    #
    def delete(self, key: str) -> bool:
        return self.forget(key)

    # Get an item from the cache, or execute the given Closure and store the result.
    def remember(self, key: str, ttl: int, callback: callable) -> any:
        value_ = self.get(key)

        # If the item exists in the cache we will just return this immediately and if
        # not we will execute the given Closure and cache the result of that for a
        # given number of seconds so it's available for all subsequent requests.
        if value_ is not None:
            return value_

        value_ = callback()

        self.put(key, value, value(ttl))

        return value_

    # Retrieve an item from the cache and delete it.
    def pull(self, key: str, default: any = None) -> any:
        return tap(self.get(key, default), lambda value_: self.forget(key))

    # Store multiple items in the cache for a given number of seconds.
    def set(self, key, value, ttl=None):
        return self.put(key, value, ttl)

    # Get an item from the cache, or execute the given Closure and store the result forever.
    def rememberForever(self, key: str, callback: callable) -> any:
        value_ = self.get(key)

        # If the item exists in the cache we will just return this immediately
        # and if not we will execute the given Closure and cache the result
        # of that forever so it is available for all subsequent requests.
        if value_ is not None:
            return value_

        value_ = callback()

        self.forever(key, value_)

        return value_

    #
    def deleteMultiple(self, keys: list) -> bool:
        result = True

        for key in keys:
            if not self.forget(key):
                result = False

        return result

    #
    def clear(self) -> bool:
        return self._store.flush()

    #
    def flush(self) -> bool:
        return self.clear()

    #
    def getMultiple(self, keys: list, default=None) -> iter:
        defaults = []

        for key in keys:
            defaults[key] = default

        return self.many(defaults)

    #
    def setMultiple(self, values: dict, ttl: int = None):
        return self.putMany(isinstance(values, dict) and values or dict(zip(values, [ttl] * len(values))))

    # Get an item from the cache, or execute the given Closure and store the result forever.
    def sear(self, key: str, callback: callable) -> any:
        return self.rememberForever(key, callback)

    # Begin executing a new tags operation if the store supports it.
    def tags(self, *names: list):
        if not self.supportsTags():
            raise RuntimeError('This cache store does not support tagging.')

        cache = self._store.tags(list(names))

        if self._events:
            cache.setEventDispatcher(self._events)

        return cache.setDefaultCacheTime(self._default)