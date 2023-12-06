class Store:
    # Retrieve an item from the cache by key.
    def get(self, key: str | list) -> any:
        pass

    # Retrieve multiple items from the cache by key.
    # Items not found in the cache will have a null value.
    def many(self, keys: list) -> dict:
        pass

    # Store an item in the cache for a given number of minutes.
    def put(self, key: str, value: any, seconds: int) -> bool:
        pass

    # Store multiple items in the cache for a given number of seconds.
    def putMany(self, values: dict, seconds: int) -> bool:
        pass

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> int:
        pass

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> int:
        pass

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value: any) -> bool:
        pass

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        pass

    # Remove all items from the cache.
    def flush(self) -> bool:
        pass

    # Get the cache key prefix.
    def getPrefix(self) -> str:
        pass
