from pythoniq.framework.illuminate.support.higherOrderTapProxy import HigherOrderTapProxy
from pythoniq.framework.illuminate.support.str import Str


# Gets the value of an environment variable.
def env(key: str, value=None) -> any:
    from pythoniq.framework.illuminate.support.env import Env
    return Env().get(key, value)


# Return the given value, optionally passed through the given callback.
def with_(value, callback: callable = None):
    if callback is None:
        return value

    return callback(value)


# Call the given Closure with the given value then return the value.
def tap(value, callback: callable = None):
    if callback is None:
        return HigherOrderTapProxy(value)

    callback(value)

    return value


# Throw the given exception if the given condition is true.
def throw_if(condition: bool, exception: Exception, **args) -> any:
    if condition:
        if isinstance(exception, str):
            exception = Exception(*args)

        raise isinstance(exception, str) and Exception(exception) or exception

    return condition


def _import_(modulePath: str):
    module = __import__(Str.of(modulePath).beforeLast('.').replace('.', '/').value())
    moduleName = Str.of(modulePath).afterLast('.').studly().value()
    return getattr(module, moduleName)
