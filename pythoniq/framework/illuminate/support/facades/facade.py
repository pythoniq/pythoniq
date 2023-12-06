from pythoniq.framework.illuminate.contracts.foundation.application import Application
from pythoniq.framework.illuminate.support.defaultFacades import DefaultFacades
from pythoniq.framework.illuminate.support.testing.fakes.fake import Fake


class Facade:
    # The application instance being facaded.
    _app: Application = None

    # The resolved object instances.
    _resolvedInstance: dict = {}

    # Indicates if the resolved instance should be cached.
    _cached: bool = True

    # Run a Closure when the facade has been resolved.
    @staticmethod
    def resolved(callback: callable) -> None:
        accessor = Facade.getFacadeAccessor()

        if Facade._app.resolved(accessor):
            callback(Facade.getFacadeRoot())

        Facade._app.afterResolving(accessor, lambda service: callback(service))

    # Convert the facade into a Mockery spy.
    @staticmethod
    def spy():
        raise NotImplementedError()

    # Initiate a partial mock on the facade.
    @staticmethod
    def partialMock():
        raise NotImplementedError()

    # Initiate a mock expectation on the facade.
    @staticmethod
    def shouldReceive():
        raise NotImplementedError()

    # Initiate a mock expectation on the facade.
    @staticmethod
    def expects():
        raise NotImplementedError()

    # Create a fresh mock instance for the given class.
    @staticmethod
    def createFreshMockInstance():
        raise NotImplementedError()

    # Create a fresh mock instance for the given class.
    @staticmethod
    def createMock():
        raise NotImplementedError()

    # Determines whether a mock is set as the instance of the facade.
    @staticmethod
    def isMock():
        raise NotImplementedError()

    # Get the mockable class for the bound instance.
    @staticmethod
    def getMockableClass():
        raise NotImplementedError()

    # Hotswap the underlying instance behind the facade.
    @staticmethod
    def swap(instance: any) -> None:
        Facade._resolvedInstance[Facade.getFacadeAccessor()] = instance

        if Facade._app is not None:
            Facade._app.instance(Facade.getFacadeAccessor(), instance)

    # Determines whether a "fake" has been set as the facade instance.
    @staticmethod
    def isFake():
        name = Facade.getFacadeAccessor()

        return name in Facade._resolvedInstance and isinstance(Facade._resolvedInstance[name], Fake)

    # Get the root object behind the facade.
    @staticmethod
    def getFacadeRoot():
        return Facade.resolveFacadeInstance(Facade.getFacadeAccessor())

    # Get the registered name of the component.
    @staticmethod
    def getFacadeAccessor() -> str:
        raise RuntimeError("Facade does not implement getFacadeAccessor method.")

    # Resolve the facade root instance from the container.
    @staticmethod
    def resolveFacadeInstance(name: str):
        if name in Facade._resolvedInstance:
            return Facade._resolvedInstance[name]

        if Facade._app:
            if Facade._cached:
                Facade._resolvedInstance[name] = Facade._app[name]
                return Facade._resolvedInstance[name]

            return Facade._app[name]

    # Clear a resolved facade instance.
    @staticmethod
    def clearResolvedInstance(name: str) -> None:
        if name in Facade._resolvedInstance:
            Facade._resolvedInstance.pop(name, None)

    # Clear all of the resolved instances.
    @staticmethod
    def clearResolvedInstances() -> None:
        Facade._resolvedInstance = {}

    # Get the application default aliases.
    @staticmethod
    def defaultFacades() -> DefaultFacades:
        return DefaultFacades()

    # Get the application instance behind the facade.
    @staticmethod
    def getFacadeApplication() -> Application:
        return Facade._app

    # Set the application instance.
    @staticmethod
    def setFacadeApplication(app: Application) -> None:
        Facade._app = app

    # Handle dynamic, static calls to the object.
    @staticmethod
    def __callStatic(method: str, args: list) -> any:
        instance = Facade.getFacadeRoot()

        if instance is None:
            raise RuntimeError("A facade root has not been set.")

        return getattr(instance, method)(*args)

    # Dynamically proxy method calls to the underlying logger.
    def __getattr__(self, method: str) -> any:
        instance = self.getFacadeRoot()

        if instance is None:
            raise RuntimeError("A facade root has not been set.")

        def _missing(*args):
            return getattr(instance, method)(*args)

        return _missing
