from pythoniq.framework.illuminate.contracts.cache.store import Store


class Repository:
    # Retrieve an item from the cache and delete it.
    def pull(self, key: str, default: any = None) -> any:
        pass

    # Store an item in the cache.
    def put(self, key: str, value: any, ttl: int = None) -> bool:
        pass

    # Store an item in the cache if the key does not exist.
    def add(self, key: str, value: any, ttl: int = None) -> bool:
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

    # Get an item from the cache, or execute the given Closure and store the result.
    def remember(self, key: str, ttl: int, callback: callable) -> any:
        pass

    # Get an item from the cache, or execute the given Closure and store the result forever.
    def sear(self, key: str, callback: callable) -> any:
        pass

    # Get an item from the cache, or execute the given Closure and store the result forever.
    def rememberForever(self, key: str, callback: callable) -> any:
        pass

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        pass

    # Get the cache store implementation.
    def getStore(self) -> Store:
        pass
