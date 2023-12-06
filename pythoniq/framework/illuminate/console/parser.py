class Parser:
    # Parse the given console command definition into an array.
    @staticmethod
    def parse(command: object) -> list:
        name = Parser._name(command)

        raise NotImplementedError

    # Extract the name of the command from the expression.
    @staticmethod
    def _name(command: object) -> str:
        raise NotImplementedError

    # Extract all of the arguments from the expression.
    @staticmethod
    def _arguments(command: object) -> list:
        raise NotImplementedError

    # Parse an argument expression.
    @staticmethod
    def _parseArgument(argument: str) -> list:
        raise NotImplementedError

    # Parse an option expression.
    @staticmethod
    def _parseOption(option: str) -> list:
        raise NotImplementedError

    # Parse the token its token and description segments.
    @staticmethod
    def _extractDescription(token: str) -> list:
        raise NotImplementedError
