from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem


class Factory:
    # Get a filesystem implementation.
    def disk(self, name: str = None) -> Filesystem:
        pass
