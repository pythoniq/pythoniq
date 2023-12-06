class Filesystem:
    # The public visibility setting.
    VISIBILITY_PUBLIC = "public"

    # The private visibility setting.
    VISIBILITY_PRIVATE = "private"

    # Determine if a file exists.
    def exists(self, path: str) -> bool:
        pass

    # Get the contents of a file.
    def get(self, path: str, lock=False) -> str | None:
        pass

    # Get a resource to read the file.
    def readStream(self, path: str):
        pass

    # Write the contents of a file.
    def put(self, path: str, contents: str | bytes, options: dict = {}):
        pass

    # Write a new file using a stream.
    def putStream(self, path: str, resource, options: dict = {}):
        pass

    # Get the visibility for the given path.
    def getVisibility(self, path: str) -> str:
        pass

    # Set the visibility for the given path.
    def setVisibility(self, path: str, visibility: str):
        pass

    # Prepend to a file.
    def prepend(self, path: str, data: str):
        pass

    # Append to a file.
    def append(self, path: str, data: str):
        pass

    # Delete the file at a given path.
    def delete(self, paths: str | list):
        pass

    # Copy a file to a new location.
    def copy(self, from_: str, to: str):
        pass

    # Move a file to a new location.
    def move(self, from_: str, to: str):
        pass

    # Get the file size of a given file.
    def size(self, path: str) -> int:
        pass

    # Get the file's last modification time.
    def lastModified(self, path: str) -> int:
        pass

    # Get an array of all files in a directory.
    def files(self, directory: str, hidden: bool = False) -> list:
        pass

    # Get all of the files from the given directory (recursive).
    def allFiles(self, directory: str, recursive: bool = False) -> list:
        pass

    # Get all of the directories within a given directory.
    def directories(self, directory: str, recursive: bool = False) -> list:
        pass

    # Create a directory.
    def makeDirectory(self, path: str, recursive: bool = False, force: bool = False) -> bool:
        pass

    # Recursively delete a directory.
    def deleteDirectory(self, directory: str, preserve: bool = False) -> bool:
        pass

    # Determine if the given path is a directory.
    def isDirectory(self, directory: str) -> bool:
        pass

    # Determine if the given path is a file.
    def isFile(self, file: str) -> bool:
        pass

    def listDir(self, path) -> list[str]:
        pass

    # Ensure a directory exists.
    def ensureDirectoryExists(self, directory: str, recursive: bool = False) -> bool:
        pass
