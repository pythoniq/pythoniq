from pythoniq.framework.illuminate.support.facades.facade import Facade


class Log(Facade):
    # Get the root object behind the facade.
    @staticmethod
    def getFacadeRoot():
        return Facade.resolveFacadeInstance(Log.getFacadeAccessor())

    # Get the registered name of the component.
    @staticmethod
    def getFacadeAccessor() -> str:
        return 'log'
