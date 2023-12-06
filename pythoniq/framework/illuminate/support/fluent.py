from pythoniq.framework.illuminate.contracts.support.arrayable import Arrayable
from pythoniq.framework.illuminate.contracts.support.jsonable import Jsonable
from pythoniq.framework.illuminate.collections.helpers import value

import json


class Fluent(dict, Arrayable, Jsonable):
    # All of the attributes set on the fluent instance.
    _attributes: dict = {}

    # Create a new fluent instance.
    def __init__(self, attributes: dict = {}):
        super().__init__()
        for key, value in attributes.items():
            self._attributes[key] = value

    # Get an attribute from the fluent instance.
    def get(self, key, default=None):
        if key in self._attributes:
            return self._attributes[key]

        return value(default)

    # Get the attributes from the fluent instance.
    def getAttributes(self):
        return self._attributes

    # Convert the fluent instance to an array.
    def toArray(self):
        return self._attributes

    # Convert the object into something JSON serializable.
    def jsonSerialize(self):
        return self.toArray()

    # Convert the fluent instance to JSON.
    def toJson(self, options=0):
        return json.dumps(self.jsonSerialize())

    # Determine if a given offset exists.
    def offsetExists(self, key: str) -> bool:
        return key in self._attributes

    # Get the value at a given offset.
    def offsetGet(self, key: str) -> any:
        return self.get(key)

    # Set the value at a given offset.
    def offsetSet(self, key: str, value: any) -> None:
        self._attributes[key] = value

    # Unset the value at a given offset.
    def offsetUnset(self, key: str) -> None:
        self._attributes.pop(key, None)

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

    # Dynamically check if an attribute is set.
    def __isset__(self, key: str) -> bool:
        return self.offsetExists(key)
