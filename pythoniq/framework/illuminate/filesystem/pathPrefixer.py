class PathPrefixer:
    # Path prefix
    _prefix: str = ''

    # Path separator
    _separator: str = '/'

    # Create a new path prefixer instance.
    def __init__(self, prefix: str, separator: str = '/') -> None:
        self._prefix = prefix.rstrip(separator)

        if self._prefix == '' or self._prefix != separator:
            self._prefix += separator

    def prefixPath(self, path: str) -> str:
        return self._prefix + path.lstrip(self._separator)

    def stripPrefix(self, path: str) -> str:
        if self._prefix == self._separator:
            return path

        return path[len(self._prefix) - 1:]

    def stripDirectoryPrefix(self, path: str) -> str:
        return self.stripPrefix(path).rstrip(self._separator)

    def prefixDirectoryPath(self, path: str) -> str:
        prefixedPath = self.prefixPath(path.rstrip(self._separator))

        if prefixedPath == '' or prefixedPath[-1] == self._separator:
            return prefixedPath

        return prefixedPath + self._separator
