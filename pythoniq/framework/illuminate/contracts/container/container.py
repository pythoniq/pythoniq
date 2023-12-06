from pythoniq.framework.illuminate.contracts.container.contextualBindingBuilder import ContextualBindingBuilder


class Container:
    # Determine if the given abstract type has been bound.
    def bound(self, abstract: str) -> bool:
        pass

    # Alias a type to a different name.
    def alias(self, abstract: str, alies: str) -> None:
        pass

    # Assign a set of tags to a given binding.
    def tag(self, abstract: list | str, tag: list | str) -> None:
        pass

    # Resolve all of the bindings for a given tag.
    def tagged(self, tag: str) -> str:
        pass

    # Register a binding with the container.
    def bind(self, abstract: str, concrete: callable | str | None = None, shared: bool = False) -> str:
        pass

    # Bind a callback to resolve with Container::call.
    def bindMethod(self, method: list | str, callback: callable):
        pass

    # Register a binding if it hasn't already been registered.
    def bindIf(self, abstract: str, concrete: callable | str | None = None, shared: bool = False) -> None:
        pass

    # Register a shared binding in the container.
    def singleton(self, abstract: str, concrete: callable | str | None = None) -> None:
        pass

    # Register a shared binding if it hasn't already been registered.
    def singletonIf(self, abstract: str, concrete: callable | str | None = None) -> None:
        pass

    # Register a scoped binding in the container.
    def scoped(self, abstract: str, concrete: callable | str | None = None) -> None:
        pass

    # Register a scoped binding if it hasn't already been registered.
    def scopedIf(self, abstract: str, concrete: callable | str | None = None) -> None:
        pass

    # "Extend" an abstract type in the container.
    def extend(self, abstract: str, closure: callable) -> None:
        pass

    # Register an existing instance as shared in the container.
    def instance(self, abstract: str, instance) -> any:
        pass

    # Add a contextual binding to the container.
    def addContextualBinding(self, concrete: str, abstract: str, implementation: callable | str) -> None:
        pass

    # Define a contextual binding.
    def when(self, concrete: str | list) -> ContextualBindingBuilder:
        pass

    # Get a closure to resolve the given type from the container.
    def factory(self, abstract: str) -> callable:
        pass

    # Flush the container of all bindings and resolved instances.
    def flush(self) -> None:
        pass

    # Resolve the given type from the container.
    def make(self, abstract: str | callable, parameters: list = []) -> any:
        pass

    # Call the given Closure / class@method and inject its dependencies.
    def call(self, callback: str | callable, parameters: list = [], defaultMethod: str | None = None):
        pass

    # Determine if the given abstract type has been resolved.
    def resolved(self, abstract: str) -> bool:
        pass

    # Register a new before resolving callback.
    def beforeResolving(self, abstract: callable | str, callback: callable | None = None) -> None:
        pass

    # Register a new resolving callback.
    def resolving(self, abstract: callable | str, callback: callable | None = None) -> None:
        pass

    # Register a new after resolving callback.
    def afterResolving(self, abstract: callable | str, callback: callable | None = None) -> None:
        pass
