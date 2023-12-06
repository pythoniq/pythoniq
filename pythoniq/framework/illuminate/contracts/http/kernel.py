from pythoniq.framework.illuminate.contracts.foundation.application import Application


class Kernel:
    # Bootstrap the application for HTTP requests.
    def bootstrap(self) -> None:
        pass

    # Handle an incoming HTTP request.
    def handle(self, request) -> any:
        pass

    # Perform any final actions for the request lifecycle.
    def terminate(self, input, status: int) -> None:
        pass

    # Get the Laravel application instance.
    def getApplication(self) -> Application:
        pass
