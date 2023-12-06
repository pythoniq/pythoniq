from pythoniq.framework.illuminate.cache.fileLock import FileLock
from pythoniq.framework.illuminate.contracts.cache.lock import Lock
from pythoniq.framework.illuminate.contracts.cache.store import Store
from pythoniq.framework.illuminate.contracts.cache.lockProvider import LockProvider
from pythoniq.framework.illuminate.contracts.filesystem.lockTimeoutException import LockTimeoutException
from pythoniq.framework.illuminate.filesystem.lockableFile import LockableFile
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.helpers import tap
from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.cache.retrievesMultipleKeys import RetrievesMultipleKeys
from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem as FilesystemContract
from pythoniq.framework.illuminate.support.str import Str
from lib.phpserialize import serialize, unserialize


class FileStore(Store, LockProvider, InteractsWithTime, RetrievesMultipleKeys):
    # The Illuminate Filesystem instance.
    _files: FilesystemContract = None

    # The file cache directory.
    _directory: str = None

    # The file cache lock directory.
    _lockDirectory: str = None

    # Octal representation of the cache file permissions.
    _filePermissions: int = None

    # Create a new file cache store instance.
    def __init__(self, files: FilesystemContract, directory: str, filePermissions: int = None):
        self._files = files
        self._directory = directory
        self._filePermissions = filePermissions or 0o644

    # Retrieve an item from the cache by key.
    def get(self, key: str) -> any:
        return self._getPayload(key)['data'] or None

    # Store an item in the cache for a given number of seconds.
    def put(self, key: str, value: any, seconds: int = None) -> bool:
        path = self.path(key)
        self._ensureCacheDirectoryExists(path)

        result = self._files.put(path, str(self._expiration(seconds)) + serialize(value))

        if result:
            self._ensurePermissionsAreCorrect(path)

            return True

        return False

    # Store an item in the cache if the key doesn't exist.
    def add(self, key: str, value: any, seconds: int) -> bool:
        path = self.path(key)
        self._ensureCacheDirectoryExists(path)

        file = LockableFile(path, 'c+b')

        try:
            file.getExclusiveLock()
        except LockTimeoutException:
            file.close()

            return False

        expire = file.read(10)

        if not expire or self._currentTime() >= expire:
            file.truncate().write(self._expiration(seconds) + serialize(value)).close()

            self._ensurePermissionsAreCorrect(path)

            return True

        file.close()

        return False

    # Create the file cache directory if necessary.
    def _ensureCacheDirectoryExists(self, path: str) -> None:
        directory = Str.dirname(path)

        if not self._files.exists(directory):
            self._files.makeDirectory(directory, True, True)

            # We're creating two levels of directories (e.g. 7e/24), so we check them both...
            self._ensurePermissionsAreCorrect(directory)
            self._ensurePermissionsAreCorrect(Str.dirname(directory))

    # Ensure the created node has the correct permissions.
    def _ensurePermissionsAreCorrect(self, path: str) -> None:
        # @todo: check if this is correct
        pass

    # Increment the value of an item in the cache.
    def increment(self, key: str, value: int = 1) -> int:
        raw = self._getPayload(key)

        return tap(int(raw['data']) + value, lambda newValue: self.put(key, newValue, raw['time'] or 0))

    # Decrement the value of an item in the cache.
    def decrement(self, key: str, value: int = 1) -> int:
        return self.increment(key, -value)

    # Store an item in the cache indefinitely.
    def forever(self, key: str, value: any) -> bool:
        return self.put(key, value, 9999999299)

    # Get a lock instance.
    def lock(self, name: str, seconds: int = 0, owner: str = None) -> Lock:
        self._ensureCacheDirectoryExists(self._lockDirectory or self._directory)

        return FileLock(FileStore(self._files, self._lockDirectory or self._directory), name, seconds, owner)

    # Restore a lock instance using the owner identifier.
    def restoreLock(self, name: str, owner: str) -> Lock:
        return self.lock(name, 0, owner)

    # Remove an item from the cache.
    def forget(self, key: str) -> bool:
        file = self.path(key)
        if self._files.exists(file):
            return self._files.delete(file)

        return False

    # Remove all items from the cache.
    def flush(self) -> bool:
        if not self._files.deleteDirectory(self._directory):
            return False

        for directory in self._files.directories(self._directory):
            deleted = self._files.deleteDirectory(directory)

            if not deleted or self._files.exists(directory):
                return False

        return True

    # Retrieve an item and expiry time from the cache by key.
    def _getPayload(self, key: str) -> dict:
        path = self.path(key)

        # If the file doesn't exist, we obviously cannot return the cache so we will
        # just return null. Otherwise, we'll get the contents of the file and get
        # the expiration UNIX timestamps from the start of the file's contents.
        try:
            contents = self._files.get(path)
            expire = Str.substr(contents, 0, 10)
        except Exception:
            return self._emptyPayload()

        # If the current time is greater than expiration timestamps we will delete
        # the file and return null. This helps clean up the old files and keeps
        # this directory much cleaner for us as old files aren't hanging out.
        if self._currentTime() >= int(expire):
            self.forget(key)

            return self._emptyPayload()

        try:
            data = unserialize(Str.substr(contents, 10))
        except Exception:
            self.forget(key)

            return self._emptyPayload()

        # Next, we'll extract the number of seconds that are remaining for a cache
        # so that we can properly retain the time for things like the increment
        # operation that may be performed on this cache on a later operation.
        time = int(expire) - self._currentTime()

        return {'data': data, 'time': time}

    # Get a default empty payload for the cache.
    def _emptyPayload(self) -> dict:
        return {'data': None, 'time': None}

    # Get the full path for the given cache key.
    def path(self, key: str) -> str:
        hash = App().hash().driver('sha1').make(key).decode('utf-8')
        length = 2
        parts = [hash[y - length:y] for y in range(length, len(hash) + length, length)]
        parts = parts[:length]

        return self._directory + '/' + '/'.join(parts) + '/' + hash + '.txt'

    # Get the expiration time based on the given seconds.
    def _expiration(self, seconds: int) -> int:
        time = self._availableAt(seconds)

        if seconds == 0:
            if time > 9999999999:
                return 9999999999

        return time

    # Get the Filesystem instance.
    def getFilesystem(self) -> FilesystemContract:
        return self._files

    # Get the working directory of the cache.
    def getDirectory(self) -> str:
        return self._directory

    # Set the cache directory where locks should be stored.
    def setLockDirectory(self, directory: str | None):
        self._lockDirectory = directory

        return self

    # Get the cache key prefix.
    def getPrefix(self) -> str:
        return ''
