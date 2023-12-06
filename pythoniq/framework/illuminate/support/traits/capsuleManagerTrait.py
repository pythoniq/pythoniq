from pythoniq.framework.illuminate.contracts.container.container import Container as ContainerContract
from pythoniq.framework.illuminate.support.fluent import Fluent


class CapsuleManagerTrait:
    # The current globally used instance.
    _instance = None

    # The container instance.
    _container: ContainerContract = None

    # Setup the IoC container instance.
    def _setupContainer(self, container: ContainerContract):
        self._container = container

        if not self._container.bound('config'):
            self._container.instance('config', Fluent())

    # Make this capsule instance available globally.
    def setAsGlobal(self):
        self._instance = self

    # Get the IoC container instance.
    def getContainer(self) -> ContainerContract:
        return self._container

    # Set the IoC container instance.
    def setContainer(self, container: ContainerContract):
        self._container = container
