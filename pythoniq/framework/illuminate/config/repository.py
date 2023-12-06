from pythoniq.framework.illuminate.contracts.config.repository import Repository as ConfigContract
from pythoniq.framework.illuminate.support.traits.macroable import Macroable
from pythoniq.framework.illuminate.collections.arr import Arr


class Repository(ConfigContract, Macroable):
    # All of the configuration items.
    _items: dict = {}

    def __init__(self, items: dict):
        self._items = items

    # Determine if the given configuration value exists.
    def has(self, key: str) -> bool:
        return Arr.has(self._items, key)

    # Get the specified configuration value.
    def get(self, key: str | list, default: any = None) -> any:
        if isinstance(key, list):
            return self.getMany(key)

        return Arr.get(self._items, key, default)

    # Get many configuration values.
    def getMany(self, keys: list) -> dict:
        config = {}

        for key in keys:
            if isinstance(key, int):
                [key, default] = [keys[key], None]

                config[key] = Arr.get(self._items, key, default)

        return config

    # Set a given configuration value.
    def set(self, key: str, value: any = None) -> None:
        keys = key
        if not isinstance(key, dict):
            keys = {key: value}

        for key, value in keys.items():
            self._items = Arr.set(self._items, key, value)

    # Forget a given configuration value.
    def forget(self, keys: str) -> None:
        if not isinstance(keys, list):
            keys = [keys]

        for key in keys:
            self._items = Arr.forget(self._items, key)

    # Prepend a value onto an array configuration value.
    def prepend(self, key: str, value: dict) -> None:
        data = self.get(key, [])

        data.update(value)

        self.set(key, data)

    # Push a value onto an array configuration value.
    def push(self, key: str, value: dict) -> None:
        data = self.get(key, [])

        data.append(value)

        self.set(key, data)

    # Get all of the configuration items for the application.
    def all(self) -> dict:
        return self._items

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
