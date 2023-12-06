class CommandContract:
    @classmethod
    def getSignature(cls) -> str:
        pass

    @classmethod
    def getDescription(cls) -> str:
        pass

    @classmethod
    def getTimeout(cls) -> int:
        pass

    @classmethod
    def getPrefix(cls) -> str:
        pass

    # The mobile equipment returns the list of parameters and value ranges set with
    # the corresponding to Write Command or by internal processes.
    @classmethod
    def test(cls) -> str:
        pass

    # This command returns the currently set value of the parameter or parameters.
    @classmethod
    def read(cls) -> str:
        pass

    # This command sets the user-definable parameter values.
    @classmethod
    def write(cls, command: str) -> str:
        pass

    # The execution command reads non-variable parameters affected by internal processes in the GSM engine.
    @classmethod
    def execute(cls) -> str:
        pass

    @classmethod
    def prefixCommand(cls) -> str:
        pass

