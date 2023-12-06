from pythoniq.framework.illuminate.cache.repository import Repository
from pythoniq.framework.illuminate.contracts.cache.factory import Factory as FactoryContract
from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.support.helpers import tap
from pythoniq.framework.illuminate.support.manager import Manager


class CacheManager(FactoryContract, Manager):
    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('cache.default', 'file')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('cache.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        if name is None or name == '' or name == 'None' or name == 'null':
            return {"driver": 'null'}

        return self._app['config'][f'cache.stores.{name}']

    # Drivers

    # Create an instance of the array cache driver.
    def createArrayDriver(self, config: dict) -> Repository:
        from pythoniq.framework.illuminate.cache.arrayStore import ArrayStore

        return self.repository(ArrayStore(config['serialize'] or False))

    # Create an instance of the file cache driver.
    def createFileDriver(self, config: dict) -> Repository:
        from pythoniq.framework.illuminate.cache.fileStore import FileStore
        store = (FileStore(self._app['files'], config['path'], config.get('permission', None))
                 .setLockDirectory(config['lock_path'] or None))
        return self.repository(store)

    # Create an instance of the array cache driver.
    def createNullDriver(self, config: dict) -> Repository:
        from pythoniq.framework.illuminate.cache.nullStore import NullStore

        return self.repository(NullStore())

    def repository(self, store: Store) -> Repository:
        return tap(Repository(store), lambda repository: self._setEventDispatcher(repository))

    # Events

    # Set the event dispatcher on the given repository instance.
    def _setEventDispatcher(self, repository: Repository) -> None:
        if not self._app.bound('events'):
            return

        repository.setEventDispatcher(self._app['events'])

    # Re-set the event dispatcher on all resolved cache repositories.
    def refreshEventDispatcher(self) -> None:
        for name, repository in self._drivers.items():
            self._setEventDispatcher(repository)

    # Methods

    # Retrieve an item from the cache by key.
    def get(self, key: str | list) -> any:
        return self.driver().get(key)

    # Retrieve multiple items from the cache by key.
    # Items not found in the cache will have a null value.
    def many(self, keys: list) -> dict:
        return self.driver().many(keys)

    # Store an item in the cache for a given number of minutes.
    def put(self, key: str, value: any, seconds: int = None) -> bool:
        return self.driver().put(key, value, seconds)

    # Store multiple items in the cache for a given number of seconds.
    def putMany(self, values: dict, seconds: int) -> bool:
        return self.driver().putMany(values, seconds)

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> int:
        return self.driver().increment(key, value)

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> int:
        return self.driver().decrement(key, value)

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value: any) -> bool:
        return self.driver().forever(key, value)

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        return self.driver().forget(key)

    # Remove all items from the cache.
    def flush(self) -> bool:
        return self.driver().flush()

    # Get the cache key prefix.
    def getPrefix(self) -> str:
        return self.driver().getPrefix()
