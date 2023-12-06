from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem as FilesystemContract
from pythoniq.framework.illuminate.support.traits.conditionable import Conditionable
from pythoniq.framework.illuminate.support.traits.macroable import Macroable
from pythoniq.framework.illuminate.filesystem.pathPrefixer import PathPrefixer
from pythoniq.framework.illuminate.support.helpers import throw_if
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.str import Str
from pythoniq.framework.illuminate.contracts.filesystem.fileNotFoundException import FileNotFoundException


class AbstractFilesystem(FilesystemContract, Conditionable, Macroable):
    # The filesystem configuration.
    _config: dict = None

    # The Flysystem PathPrefixer instance.
    _prefixer: PathPrefixer = None

    # The array of created "read" streams.
    _streams = {}

    def __init__(self, config: dict = None) -> None:
        self._config = config or {}
        seperator = config.get('separator', '/')
        self._prefixer = PathPrefixer(config.get('root', ''), seperator)

        if 'prefix' in config:
            self._prefixer = PathPrefixer(self._prefixer.prefixPath(config.get('prefix')), seperator)

    # Determine if a file or directory is missing.
    def missing(self, path: str) -> bool:
        return not self.exists(path)

    # Get the contents of a file as decoded JSON.
    def json(self, path: str, lock=False) -> dict:
        import json
        return json.loads(self.get(path))

    # Get contents of a file with shared access.
    # @todo: Implement this method.
    def sharedGet(self, path: str) -> str:
        return self.get(path, True)

    # Get the hash of the file at the given path.
    def hash(self, path: str, algorithm: str = 'sha256') -> str:
        return App().hash().driver(algorithm).make(self.get(path))

    # Write the contents of a file, replacing it atomically if it already exists.
    def replace(self, path: str, contents: str, mode: int = None) -> bool:
        raise NotImplementedError(__name__ + ' replace')

    # Replace a given string within a given file.
    def replaceInFile(self, search: str, replace: str, path: str) -> bool:
        return self.put(path, self.get(path).replace(search, replace))

    # Prepend to a file.
    def prepend(self, path: str, data: str) -> bool:
        if self.exists(path):
            return self.put(path, data + self.get(path))

        return self.put(path, data)

    # Copy a file to a new location.
    def copy(self, path: str, target: str) -> bool:
        try:
            if self.isDirectory(path):
                raise FileNotFoundException('File does not exist at path "%s".' % path)

            self.put(target, self.get(path))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Create a symlink to the target file or directory. On Windows, a hard link is created if the target is a file.
    def link(self, target: str, link: str) -> bool:
        raise NotImplementedError(__name__ + ' link')

    # Create a relative symlink to the target file or directory.
    def relativeLink(self, target: str, link: str) -> bool:
        raise NotImplementedError(__name__ + ' relativeLink')

    # Extract the file name from a file path.
    def name(self, path: str) -> str:
        return Str.name(path)

    # Extract the trailing name component from a file path.
    def basename(self, path: str) -> str:
        return Str.basename(path)

    # Extract the parent directory from a file path.
    def dirname(self, path: str) -> str:
        return Str.dirname(path)

    # Extract the file extension from a file path.
    def extension(self, path: str) -> str:
        return Str.extension(path)

    # Guess the file extension from the mime-type of a given file.
    def guessExtension(self) -> str:
        raise NotImplementedError(__name__ + ' guessExtension')

    # Get the file type of a given file.
    def type(self) -> str:
        raise NotImplementedError(__name__ + ' fileType')

    #  Get the mime-type of a given file.
    def mimeType(self) -> str:
        raise NotImplementedError(__name__ + ' mimeType')

    # Determine if the given path is a directory that does not contain any other files or directories.
    def isEmptyDirectory(self, directory: str) -> bool:
        return len(self.listDir(directory)) == 0

    # Determine if the given path is readable.
    def isReadable(self, path: str) -> bool:
        return True

    # Determine if the given path is writable.
    def isWritable(self, path: str) -> bool:
        return True

    # Determine if two files are the same by comparing their hashes.
    def hasSameHash(self, firstFile: str, secondFile: str) -> bool:
        return self.hash(firstFile) == self.hash(secondFile)

    # Find path names matching a given pattern.
    def glob(self, pattern: str, flags: int = 0) -> list:
        raise NotImplementedError(__name__ + ' glob')

    # Get an array of all files in a directory.
    def files(self, directory: str, hidden: bool = False) -> list:
        items = []
        for item in self.listDir(directory):
            if self.isFile(directory + '/' + item):
                items.append(item)

        return list(filter(lambda item: not item.startswith('.') or hidden, items))

    # Get all of the files from the given directory (recursive).
    def allFiles(self, directory: str, hidden: bool = False) -> list:
        items = []
        for item in self.listDir(directory):
            if self.isFile(directory + '/' + item):
                items.append(item)

            if self.isDirectory(directory + '/' + item):
                for file in self.allFiles(directory + '/' + item, hidden):
                    items.append(item + '/' + file)

        return items

    # Get all of the directories within a given directory.
    def directories(self, directory: str, recursive: bool = False) -> list:
        items = []
        for item in self.listDir(directory):
            if self.isDirectory(directory + '/' + item):
                items.append(item)

        return items

    # Ensure a directory exists.
    def ensureDirectoryExists(self, directory: str, recursive: bool = False) -> bool:
        if self.isDirectory(directory):
            return True

        return self.makeDirectory(directory, recursive)

    # Copy a directory from one location to another.
    def copyDirectory(self, directory: str, destination: str, options: int = None) -> bool:
        if not self.isDirectory(directory):
            return False

        # If the destination directory does not actually exist, we will go ahead and
        # create it recursively, which just gets the destination prepared to copy
        # the files over. Once we make the directory we'll proceed the copying.
        self.ensureDirectoryExists(destination)

        items = self.listDir(directory)

        for item in items:
            # As we spin through items, we will check to see if the current file is actually
            # a directory or a file. When it is actually a directory we will need to call
            # back into this function recursively to keep copying these nested folders.
            target = item
            if not destination.startswith('/'):
                target = destination + '/' + item

            if self.isDirectory(item):
                if not self.copyDirectory(item, target, options):
                    return False

            # If the current items is just a regular file, we will just copy this to the new
            # location and keep looping. If for some reason the copy fails we'll bail out
            # and return false, so the developer is aware that the copy process failed.
            elif not self.copy(item, target):
                return False

        return True

    # Remove all of the directories within a given directory.
    def deleteDirectories(self, directory: str) -> bool:
        allDirectories = self.directories(directory)

        if not len(allDirectories) == 0:
            for directory in allDirectories:
                self.deleteDirectory(directory)

            return True

        return False

    # Empty the specified directory of all files and folders.
    def cleanDirectory(self, directory: str) -> bool:
        return self.deleteDirectory(directory, True)

    # Determine if Flysystem exceptions should be thrown.
    def throwsExceptions(self) -> bool:
        return bool(self._config.get('throw', False))

    # Join the given paths together.
    def path(self, path: str = '') -> str:
        if path != '':
            return self._config['root'] + '/' + path.lstrip('/')

        return self._config['root']
