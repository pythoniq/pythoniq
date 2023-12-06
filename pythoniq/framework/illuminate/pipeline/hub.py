from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.contracts.pipeline.hub import Hub as HubContract
from pythoniq.framework.illuminate.pipeline.pipeline import Pipeline


class Hub(HubContract):
    # The container implementation.
    _container: Container | None = None

    # All of the available pipelines.
    _pipelines: dict = {}

    # Create a new Hub instance.
    def __init__(self, container: Container = None):
        self._container = container

    # Define the default named pipeline.
    def defaults(self, callback: callable):
        self.pipeline("default", callback)

    # Define a new named pipeline.
    def pipeline(self, name: str, callback: callable):
        self._pipelines[name] = callback

    # Send an object through one of the available pipelines.
    def pipe(self, object: any, pipeline: str = None):
        pipeline = pipeline or "default"

        return getattr(self._pipelines[pipeline], Pipeline(self._container))

    # Get the container instance used by the hub.
    def getCotainer(self) -> Container:
        return self._container

    # Set the container instance used by the hub.
    def setContainer(self, container: Container):
        self._container = container

        return self
