from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher as DispatcherContract
from pythoniq.framework.illuminate.support.traits.forwardsCalls import ForwardsCalls


class NullDispatcher(DispatcherContract, ForwardsCalls):
    # The underlying event dispatcher instance.
    _dispatcher: DispatcherContract = None

    # Create a new event dispatcher instance that does not fire.
    def __init__(self, dispatcher: DispatcherContract):
        self._dispatcher = dispatcher

    # Don't fire an event.
    def dispatch(self, event: str | object, payload={}, halt: bool = False) -> dict | None:
        pass

    # Don't register an event and payload to be fired later.
    def push(self, event: str, payload={}):
        pass

    # Don't dispatch an event.
    def until(self, event: str | object, payload={}) -> None:
        pass

    # Register an event listener with the dispatcher.
    def listen(self, events: callable | str | dict, listener: callable | str | dict | None = None) -> None:
        return self._dispatcher.listen(events, listener)

    # Determine if a given event has listeners.
    def hasListeners(self, eventName: str) -> bool:
        return self._dispatcher.hasListeners(eventName)

    # Register an event subscriber with the dispatcher.
    def subscribe(self, subscriber: object | str) -> None:
        self._dispatcher.subscribe(subscriber)

    # Flush a set of pushed events.
    def flush(self, event: str) -> None:
        self._dispatcher.flush(event)

    # Remove a set of listeners from the dispatcher.
    def forget(self, event: str) -> None:
        self._dispatcher.forget(event)

    # Forget all of the queued listeners.
    def forgetPushed(self) -> None:
        self._dispatcher.forgetPushed()
