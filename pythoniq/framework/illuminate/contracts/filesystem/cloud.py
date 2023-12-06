from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem


class Cloud(Filesystem):
    # Get the URL for the file at the given path.
    def url(self, path: str) -> str:
        pass
