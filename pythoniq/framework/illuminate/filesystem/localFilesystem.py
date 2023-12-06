from pythoniq.framework.illuminate.filesystem.abstractFilesystem import AbstractFilesystem
from pythoniq.framework.illuminate.contracts.filesystem.fileNotFoundException import FileNotFoundException
from pythoniq.framework.illuminate.filesystem.helpers import exists
from pythoniq.framework.illuminate.support.helpers import throw_if

from lib.helpers import is_dir, is_file
import os


class LocalFilesystem(AbstractFilesystem):
    # Determine if a file or directory exists.
    def exists(self, path: str) -> bool:
        return exists(self._prefixer.prefixPath(path))

    # Get the contents of a file.
    def get(self, path: str, lock=False) -> str:
        try:
            if not self.isFile(path):
                raise FileNotFoundException(f"File does not exist at path {path}")

            with open(self._prefixer.prefixPath(path), "r") as file:
                return file.read()
        except Exception as e:
            throw_if(self.throwsExceptions(), e)

    # Get the returned value of a file.
    def getImport(self, file):
        if self.isDirectory(file):
            raise FileNotFoundException('File does not exist at path "%s".' % file)

        return __import__(self._prefixer.prefixPath(file))

    # Get the contents of a file one line at a time.
    # @todo: LazyCollection
    def lines(self, path: str, lock=False) -> list:
        if not self.isFile(path):
            raise FileNotFoundException(f"File does not exist at path {path}")

        with open(self._prefixer.prefixPath(path), "r") as file:
            return list(map(lambda line: line.rstrip('\r\n'), file.readlines()))

    # Write the contents of a file.
    def put(self, path: str, contents: str, lock: bool = False) -> bool:
        try:
            dirname = self.dirname(path)
            if self.missing(dirname):
                self.makeDirectory(dirname, True)

            with open(self._prefixer.prefixPath(path), 'w') as file:
                file.write(contents)
                file.close()
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Append to a file.
    def append(self, path: str, data: str) -> bool:
        dirname = self.dirname(path)
        if self.missing(dirname):
            self.makeDirectory(dirname, True, True)

        hs = open(self._prefixer.prefixPath(path), 'a')
        hs.write(data)
        hs.close()

        return True

    # Get or set UNIX mode of a file or directory.
    def chmod(self, path: str, mode: int = None) -> int:
        raise NotImplementedError(__name__ + ' chmod')

    # Delete the file at a given path.
    def delete(self, path: str) -> bool:
        if self.missing(path):
            return True

        try:
            os.remove(self._prefixer.prefixPath(path))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Move a file to a new location.
    def move(self, path: str, target: str) -> bool:
        try:
            if self.isDirectory(path):
                raise FileNotFoundException('File does not exist at path "%s".' % path)

            dirname = self.dirname(path)
            if self.missing(dirname):
                self.makeDirectory(dirname)

            os.rename(self._prefixer.prefixPath(path), self._prefixer.prefixPath(target))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Get the file size of a given file.
    def size(self, path: str) -> int:
        if self.isDirectory(path):
            raise FileNotFoundException('File does not exist at path "%s".' % path)

        return self.stat(path)[6]

    # Get the file's last modification time.
    def lastModified(self, path: str) -> int:
        if self.isDirectory(path):
            raise FileNotFoundException('File does not exist at path "%s".' % path)

        return self.stat(path)[8]

    # Determine if the given path is a directory.
    def isDirectory(self, directory: str) -> bool:
        return is_dir(self._prefixer.prefixPath(directory))

    # Determine if the given path is a file.
    def isFile(self, file: str) -> bool:
        return is_file(self._prefixer.prefixPath(file))

    # Create a directory.
    def makeDirectory(self, directory: str, recursive: bool = False, force: bool = False) -> bool:
        try:
            if force and self.exists(directory):
                return True

            if recursive:
                dirname = self.dirname(directory)
                if self.missing(dirname):
                    self.makeDirectory(dirname, recursive)

            os.mkdir(self._prefixer.prefixPath(directory))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Move a directory.
    def moveDirectory(self, from_: str, to: str, overwrite: bool = False) -> bool:
        try:
            if overwrite and self.isDirectory(to) and not self.deleteDirectory(to):
                return False

            os.rename(self._prefixer.prefixPath(from_), self._prefixer.prefixPath(to))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Recursively delete a directory.
    # The directory itself may be optionally preserved.
    def deleteDirectory(self, directory: str, preserve: bool = False) -> bool:
        try:
            if not self.isDirectory(directory):
                return False

            items = self.listDir(directory)

            for item in items:
                # If the item is itself a directory, we will recursively delete it using the same
                # preserve option that was given to us, which will allow developers to delete
                # an entire directory that contains sub-directories that should be preserved.
                if self.isDirectory(directory + '/' + item):
                    self.deleteDirectory(directory + '/' + item)

                # If the item is just a file, however, we'll just unlink it since we're just
                # deleting the entire directory. We'll check for success and return out.
                else:
                    self.delete(directory + '/' + item)

            # Once we have deleted all the sub-directories and items within this directory we
            # can delete the directory itself. We will optionally re-create the directory
            # if the developer wants to preserve the directory that we have deleted.
            if not preserve:
                os.rmdir(self._prefixer.prefixPath(directory))
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    def stat(self, path: str) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        return os.stat(self._prefixer.prefixPath(path))

    def listDir(self, path) -> list[str]:
        if self.missing(path):
            raise FileNotFoundException('Directory does not exist at path "%s".' % path)

        return os.listdir(self._prefixer.prefixPath(path))

    # File open stream.
    def openStream(self, path, mode: str = 'r'):
        if path in self._streams:
            return self._streams[path]

        self._streams[path] = open(self._prefixer.prefixPath(path), mode)
        return self._streams[path]

    # Read a file as a stream.
    def writeStream(self, path: str, contents, isFlush: bool = False) -> bool:
        try:
            dirname = self.dirname(path)
            if self.missing(dirname):
                self.makeDirectory(dirname)

            self.openStream(path, 'w').write(contents)
            if isFlush:
                self._streams[path].flush()
        except Exception as e:
            throw_if(self.throwsExceptions(), e)
            return False

        return True

    # Close a file stream.
    def closeStream(self, path):
        self._streams.pop(path, None)
