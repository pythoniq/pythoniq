class Input:
    # Returns the first argument from the raw parameters (not parsed).
    def getFirstArgument(self) -> str | None:
        pass

    # Returns true if the raw parameters (not parsed) contain a value.
    def hasParameterOption(self, values: list | str, onlyParams: bool = False) -> bool:
        pass

    # Returns the value of a raw option (not parsed).
    def getParameterOption(self, values: list | str, default: any = False, onlyParams: bool = False) -> str | None:
        pass

    # Binds the current Input instance with the given arguments and options.
    def bind(self, definition) -> None:
        raise

    # Validates the input.
    def validate(self) -> None:
        pass

    # Returns all the given arguments merged with the default values.
    def getArguments(self) -> dict:
        pass

    # Returns the argument value for a given argument name.
    def getArgument(self, key: str) -> str | None:
        pass

    # Sets an argument value by name.
    def setArgument(self, key: str, value: str) -> None:
        pass

    # Returns true if an InputArgument object exists by name or position.
    def hasArgument(self, key: str) -> bool:
        pass

    # Returns all the given options merged with the default values.
    def getOptions(self) -> dict:
        pass

    # Returns the option value for a given option name.
    def getOption(self, key: str) -> str | None:
        pass

    # Sets an option value by name.
    def setOption(self, key: str, value: str) -> None:
        pass

    # Returns true if an InputOption object exists by name.
    def hasOption(self, key: str) -> bool:
        pass

    # Is this input means interactive?
    def isInteractive(self) -> bool:
        pass

    # Sets the input interactivity.
    def setInteractive(self, interactive: bool) -> None:
        pass
