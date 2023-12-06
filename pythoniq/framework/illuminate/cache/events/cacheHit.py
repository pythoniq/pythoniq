from pythoniq.framework.illuminate.cache.events.cacheEvent import CacheEvent


class CacheHit(CacheEvent):
    # The value that was retrieved.
    value: any = None

    # Create a new event instance.
    def __init__(self, key: str, value: any, tags: list = []):
        super().__init__(key, tags)

        self.value = value
