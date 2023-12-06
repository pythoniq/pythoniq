class EnvironmentDetector:
    # Detect the application's current environment.
    def detect(self, callback: callable, consoleArgs: dict = None) -> str:
        if consoleArgs:
            return self._detectConsoleEnvironment(callback, consoleArgs)

        return self._detectWebEnvironment(callback)

    # Set the application environment for a web request.
    def _detectWebEnvironment(self, callback: callable) -> str:
        return callback()

    # Set the application environment from command-line arguments.
    def _detectConsoleEnvironment(self, callback: callable, args: dict) -> str:
        # First we will check if an environment argument was passed via console arguments
        # and if it was that automatically overrides as the environment. Otherwise, we
        # will check the environment as a "web" request like a typical HTTP request.
        value = self._getEnvironmentArgument(args)
        if value:
            return value

        return self._detectWebEnvironment(callback)

    # Get the environment argument from the console.
    def _getEnvironmentArgument(self, args: dict) -> str:
        for key, value in args.items():
            if key.startswith('--env'):
                return value

        return None
