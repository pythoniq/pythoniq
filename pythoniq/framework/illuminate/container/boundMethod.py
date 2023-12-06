from pythoniq.framework.illuminate.container.util import Util


class BoundMethod:
    # Call the given Closure / class@method and inject its dependencies.
    @classmethod
    def call(cls, container, callback, parameters: list = [], defaultMethod: str = None):
        if isinstance(callback, str) and not defaultMethod and hasattr(callback, '__call__'):
            defaultMethod = '__call__'

        if cls.isCallableWithAtSign(callback) or defaultMethod:
            return cls._callClass(container, callback, parameters, defaultMethod)

        def fn():
            return callback(*parameters)

        return cls._callBoundMethod(container, callback, fn)

    # Call a string reference to a class using Class@method syntax.
    @classmethod
    def _callClass(cls, container, target, parameters: list = [], defaultMethod: str = None):
        segments = target.split('@')

        # We will assume an @ sign is used to delimit the class name from the method
        # name. We will split on this @ sign and then build a callable array that
        # we can pass right back into the "call" method for dependency binding.
        method = len(segments) == 2 and segments[1] or defaultMethod

        if not method:
            raise Exception('Method not provided.')

        return cls.call(container, [container.make(segments[0]), method], parameters)

    # Call a method that has been bound to the container.
    @classmethod
    def _callBoundMethod(cls, container, callback: callable, default: any):
        if not isinstance(callback, list):
            return Util.unwrapIfClosure(default)

        # Here we need to turn the array callable into a Class@method string we can use to
        # examine the container and see if there are any method bindings for this given
        # method. If there are, we can call this method binding callback immediately.
        method = cls._normalizeMethod(callback)

        if container.hasMethodBinding(method):
            return container.callMethodBinding(method, callback[0])

        return Util.unwrapIfClosure(default)

    # Normalize the given callback into a Class@method string.
    @classmethod
    def _normalizeMethod(cls, callback: list) -> str:
        klass = isinstance(callback[0], str) and callback[0] or callback[0].__class__.__name__

        return f'{klass}@{callback[1]}'

    # Get all dependencies for a given method.
    @classmethod
    def _getMethodDependencies(cls, container, callback, parameters: list = []) -> list:
        dependencies = []

        for parameter in cls._getCallReflector(callback).getParameters():
            cls._addDependencyForCallParameter(container, parameter, parameters, dependencies)

        return dependencies + parameters

    # Get the proper reflection instance for the given callback.
    @classmethod
    def _getCallReflector(cls, callback: callable | str):
        raise NotImplementedError

    # Get the dependency for the given call parameter.
    @classmethod
    def _addDependencyForCallParameter(cls, container, parameter, parameters: list, dependencies: list):
        raise NotImplementedError

    @staticmethod
    def isCallableWithAtSign(callback) -> bool:
        return isinstance(callback, str) and '.' in callback
