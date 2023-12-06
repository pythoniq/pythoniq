class Dispatcher:
    # Register an event listener with the dispatcher.
    def listen(self, events: callable | str | dict, listener: callable | str | dict | None = None) -> None:
        pass

    # Determine if a given event has listeners.
    def hasListeners(self, eventName: str) -> bool:
        pass

    # Register an event subscriber with the dispatcher.
    def subscribe(self, subscriber: object | str) -> None:
        pass

    # Dispatch an event until the first non-null response is returned.
    def until(self, event: str | object, payload={}) -> None:
        pass

    # Dispatch an event and call the listeners.
    def dispatch(self, event: str | object, payload={}, halt: bool = False) -> dict | None:
        pass

    # Register an event and payload to be fired later.
    def push(self, event: str, payload={}):
        pass

    # Flush a set of pushed events.
    def flush(self, event: str) -> None:
        pass

    # Remove a set of listeners from the dispatcher.
    def forget(self, event: str) -> None:
        pass

    # Forget all of the queued listeners.
    def forgetPushed(self) -> None:
        pass
