class Application:
    # Run an Artisan console command by name.
    def call(self, command: str, parameters: list = None, outputBuffer=None) -> int:
        pass

    # Get the output from the last command.
    def output(self) -> str:
        pass
