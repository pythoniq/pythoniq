class Kernel:
    # Bootstrap the application for artisan commands.
    def bootstrap(self) -> None:
        pass

    # Handle an incoming console command.
    def handle(self, input, output=None) -> int:
        pass

    # Run an Artisan console command by name.
    def call(self, command: str, parameters: list = [], output=None) -> int:
        pass

    # Queue an Artisan console command by name.
    def queue(self, command: str, parameters: list = []) -> None:
        pass

    # Get all of the commands registered with the console.
    def all(self) -> list:
        pass

    # Get the output for the last run command.
    def output(self, output) -> str:
        pass

    # Terminate the application.
    def terminate(self, input, status: int) -> None:
        pass
