from pythoniq.framework.illuminate.container.util import Util
from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.contracts.container.contextualBindingBuilder import \
    ContextualBindingBuilder as ContextualBindingBuilderContact


class ContextualBindingBuilder(ContextualBindingBuilderContact):
    # The underlying container instance.
    _container: Container = None

    # The concrete instance.
    _concrete: str | list = None

    #The abstract target.
    _needs: str = None

    def __init__(self, container: Container, concrete: str | list) -> None:
        self._container = container
        self._concrete = concrete

    # Define the abstract target that depends on the context.
    def needs(self, abstract: str):
        self._needs = abstract

        return self

    # Define the implementation for the contextual binding.
    def give(self, implementation: callable | str | list) -> None:
        for self._concrete in Util.arrayWrap(self._concrete):
            self._container.addContextualBinding(self._concrete, self._needs, implementation)

    # Define tagged services to be used as the implementation for the contextual binding.
    def giveTagged(self, tag: str) -> None:
        def fn(container: Container):
            taggedServices = container.tagged(tag)

            return taggedServices[0] if len(taggedServices) == 1 else taggedServices

        self.give(fn)

    # Specify the configuration item to bind as a primitive.
    def giveConfig(self, key: str, default=None) -> None:
        def fn(container: Container):
            return container.get('config').get(key, default)

        self.give(fn)
