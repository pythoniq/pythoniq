from pythoniq.framework.illuminate.cache.events.cacheEvent import CacheEvent


class KeyWritten(CacheEvent):
    # The value that was written.
    value: any = None

    # The number of seconds the key should be valid.
    seconds: int | None = None

    # Create a new event instance.
    def __init__(self, key: str, value: any, seconds: int | None, tags: list = []) -> None:
        super().__init__(key, tags)

        self.value = value
        self.seconds = seconds
