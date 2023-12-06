class Output:
    # Writes a message to the output.
    def write(self, message: str | iter, newline: bool = False, options: int = 0) -> None:
        pass

    # Writes a message to the output and adds a newline at the end.
    def writeln(self, message: str | iter, options: int = 0) -> None:
        pass

    # Sets the verbosity of the output.
    def setVerbosity(self, level: int) -> None:
        pass

    # Gets the current verbosity of the output.
    def getVerbosity(self) -> int:
        pass

    # Returns whether verbosity is quiet (-q)
    def isQuiet(self) -> bool:
        pass

    # Returns whether verbosity is verbose (-v)
    def isVerbose(self) -> bool:
        pass

    # Returns whether verbosity is very verbose (-vv)
    def isVeryVerbose(self) -> bool:
        pass

    # Returns whether verbosity is debug (-vvv)
    def isDebug(self) -> bool:
        pass

    # Sets the decorated flag.
    def setDecorated(self, decorated: bool) -> None:
        pass

    # Gets the decorated flag.
    def isDecorated(self) -> bool:
        pass

    # Sets output formatter.
    def setFormatter(self, formatter) -> None:
        pass

    # Returns current output formatter instance.
    def getFormatter(self) -> Formatter:
        pass
