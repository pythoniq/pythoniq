from pythoniq.framework.illuminate.support.manager import Manager
from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem as FilesystemContract


class FilesystemManager(Manager, FilesystemContract):
    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('filesystems.default', 'local')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('filesystems.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        return self._config.get('filesystems.disks.' + name, {})

    # Get a filesystem instance.
    def disk(self, name: str = None) -> FilesystemContract:
        return self.driver(name)

    # Build an on-demand log channel.
    def build(self, config: dict) -> FilesystemContract:
        self._drivers.pop('ondemand', None)

        return self._resolve('ondemand', config)

    # Get a default cloud filesystem instance.
    def cloud(self) -> FilesystemContract:
        name = self.getDefaultCloudDriver()

        self._drivers[name] = self._get(name)

        return self._drivers[name]

    # Get the filesystem connection configuration.
    def getConfig(self, name: str = None) -> dict:
        return self._config.get('filesystems.disks.{}'.format(name), {})

    # Get the default cloud driver name.
    def getDefaultCloudDriver(self) -> str:
        return self._config.get('filesystems.cloud', 's3')

    # Drivers

    # Create an instance of the Sha256 hash Driver.
    def createLocalDriver(self, config: dict) -> FilesystemContract:
        from pythoniq.framework.illuminate.filesystem.localFilesystem import LocalFilesystem

        return LocalFilesystem(config)

    # Methods

    # Determine if a file exists.
    def exists(self, path: str) -> bool:
        return self.driver().exists(path)

    # Get the contents of a file.
    def get(self, path: str, lock=False) -> str | None:
        return self.driver().get(path, lock)

    # Get a resource to read the file.
    def readStream(self, path: str):
        return self.driver().readStream(path)

    # Write the contents of a file.
    def put(self, path: str, contents: str | bytes, options: dict = {}):
        return self.driver().put(path, contents, options)

    # Write a new file using a stream.
    def putStream(self, path: str, resource, options: dict = {}):
        return self.driver().putStream(path, resource, options)

    # Get the visibility for the given path.
    def getVisibility(self, path: str) -> str:
        return self.driver().getVisibility(path)

    # Set the visibility for the given path.
    def setVisibility(self, path: str, visibility: str):
        return self.driver().setVisibility(path, visibility)

    # Prepend to a file.
    def prepend(self, path: str, data: str):
        return self.driver().prepend(path, data)

    # Append to a file.
    def append(self, path: str, data: str):
        return self.driver().append(path, data)

    # Delete the file at a given path.
    def delete(self, paths: str | list):
        return self.driver().delete(paths)

    # Copy a file to a new location.
    def copy(self, from_: str, to: str):
        return self.driver().copy(from_, to)

    # Move a file to a new location.
    def move(self, from_: str, to: str):
        return self.driver().move(from_, to)

    # Get the file size of a given file.
    def size(self, path: str) -> int:
        return self.driver().size(path)

    # Get the file's last modification time.
    def lastModified(self, path: str) -> int:
        return self.driver().lastModified(path)

    # Get an array of all files in a directory.
    def files(self, directory: str, hidden: bool = False) -> list:
        return self.driver().files(directory, hidden)

    # Get all of the files from the given directory (recursive).
    def allFiles(self, directory: str, recursive: bool = False) -> list:
        return self.driver().allFiles(directory, recursive)

    # Get all of the directories within a given directory.
    def directories(self, directory: str, recursive: bool = False) -> list:
        return self.driver().directories(directory, recursive)

    # Create a directory.
    def makeDirectory(self, path: str, recursive: bool = False, force: bool = False) -> bool:
        return self.driver().makeDirectory(path, recursive, force)

    # Recursively delete a directory.
    def deleteDirectory(self, directory: str, preserve: bool = False) -> bool:
        return self.driver().deleteDirectory(directory)

    # Determine if the given path is a directory.
    def isDirectory(self, directory: str) -> bool:
        return self.driver().isDirectory(directory)

    # Determine if the given path is a file.
    def isFile(self, file: str) -> bool:
        return self.driver().isFile(file)

    def listDir(self, path) -> list[str]:
        return self.driver().listDir(path)

    # Ensure a directory exists.
    def ensureDirectoryExists(self, directory: str, recursive: bool = False) -> bool:
        return self.driver().ensureDirectoryExists(directory, recursive)

    # File open stream.
    def openStream(self, path, mode: str = 'r'):
        return self.driver().openStream(path, path)

    # Read a file as a stream.
    def writeStream(self, path: str, contents, isFlush: bool = False) -> bool:
        return self.driver().writeStream(path, contents, isFlush)

    # Close a file stream.
    def closeStream(self, path):
        return self.driver().closeStream(path)
