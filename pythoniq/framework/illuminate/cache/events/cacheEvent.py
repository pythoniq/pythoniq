class CacheEvent:
    # The key of the event.
    key: str = None

    # The tags that were assigned to the event.
    tags: list = None

    # Create a new event instance.
    def __init__(self, key: str, tags: list = []):
        self.key = key
        self.tags = tags

    # Set the tags for the cache event.
    def setTags(self, tags: list):
        self.tags = tags

        return self
