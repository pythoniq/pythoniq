from pythoniq.framework.illuminate.filesystem.helpers import exists
from pythoniq.framework.illuminate.support.str import Str
import os


class LockableFile:
    # The file resource.
    _handle: object = None

    # The file path.
    _path: str = None

    # Indicates if the file is locked.
    _isLocked: bool = False

    # Create a new File instance.
    def __init__(self, path: str, mode: str):
        self._path = path

        self._ensureDirectoryExists(path)
        self._createResource(path, mode)

    # Create the file's directory if necessary.
    def _ensureDirectoryExists(self, path: str) -> None:
        directory = Str.dirname(path)

        if not exists(directory):
            self.makeDirectory(directory, True, True)

    def makeDirectory(self, directory: str, recursive: bool = False, force: bool = False) -> None:
        try:
            if force and exists(directory):
                return

            if recursive:
                dirname = Str.dirname(directory)
                if not exists(dirname):
                    self.makeDirectory(dirname, recursive)

            os.mkdir(directory)
        finally:
            pass

    # Create the file resource.
    def _createResource(self, path: str, mode: str) -> None:
        self.handle = open(path, mode)

        if not self.handle:
            raise Exception(
                f'Unable to create lockable file: {path} Please ensure you have permission to create files in this location.')

    # Read the file contents.
    def read(self, length: int | None = None) -> str:
        return self.handle.read(length or self.size() or 1)

    # Get the file size.
    def size(self) -> int:
        return self.handle.tell()

    # Write to the file.
    def write(self, contents: str) -> 'LockableFile':
        self.handle.write(contents)
        self.handle.flush()

        return self

    # Truncate the file.
    def truncate(self) -> 'LockableFile':
        self.close()

        self._createResource(self._path, 'w')
        self.handle.write('')
        self.handle.flush()

        return self

    # Get a shared lock on the file.
    def getSharedLock(self, block: bool = False) -> bool:
        self._isLocked = True

        return True

    # Get an exclusive lock on the file.
    def getExclusiveLock(self, block: bool = False) -> bool:
        self._isLocked = True

        return True

    # Release the lock on the file.
    def releaseLock(self) -> 'LockableFile':
        self._isLocked = False

        return self

    # Close the file.
    def close(self) -> bool:
        if self._isLocked:
            self.releaseLock()

        self.handle.close()

        return True
