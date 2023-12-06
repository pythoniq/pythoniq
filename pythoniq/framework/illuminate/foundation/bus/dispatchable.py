from pythoniq.framework.illuminate.collections.helpers import value
from pythoniq.framework.illuminate.contracts.bus.dispatcher import Dispatcher
from pythoniq.framework.illuminate.foundation.bus.pendingDispatch import PendingDispatch
from pythoniq.framework.illuminate.support.fluent import Fluent


class Dispatchable:
    # Dispatch the job with the given arguments.
    @classmethod
    def dispatch(cls, *arguments) -> PendingDispatch:
        return PendingDispatch(cls(*arguments))

    # Dispatch the job with the given arguments if the given truth test passes.
    @classmethod
    def dispatchIf(cls, boolean: bool, *arguments) -> PendingDispatch | Fluent:
        if callable(boolean):
            dispatchable = cls(*arguments)

            return value(boolean, dispatchable) and PendingDispatch(dispatchable) or Fluent()

        return value(boolean) and cls.dispatch(*arguments) or Fluent()

    # Dispatch the job with the given arguments unless the given truth test passes.
    @classmethod
    def dispatchUnless(cls, boolean: bool, *arguments) -> PendingDispatch | Fluent:
        if callable(boolean):
            dispatchable = cls(*arguments)

            return not value(boolean, dispatchable) and PendingDispatch(dispatchable) or Fluent()

        return not value(boolean) and PendingDispatch(*arguments) or Fluent()

    # Dispatch a command to its appropriate handler in the current process.
    # Queueable jobs will be dispatched to the "sync" queue.
    @classmethod
    def dispatchSync(cls, *arguments) -> any:
        return App().make(Dispatcher).dispatchSync(cls(*arguments))

    # Dispatch a command to its appropriate handler after the current process.
    @classmethod
    def dispatchAfterResponse(cls, *arguments) -> any:
        return cls.dispatch(*arguments).afterResponse()

    # Set the jobs that should run if this job is successful.
    @classmethod
    def withChain(cls, chain: list) -> PendingDispatch:
        return PendingChain(cls, chain)
