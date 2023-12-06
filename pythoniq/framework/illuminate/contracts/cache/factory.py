from pythoniq.framework.illuminate.contracts.cache.repository import Repository


class Factory:
    # Get a cache store instance by name.
    def store(self, name: str = None) -> Repository:
        pass
