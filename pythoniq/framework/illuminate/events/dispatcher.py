from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher as DispatcherContract
from pythoniq.framework.illuminate.contracts.container.container import Container as ContainerContract
from pythoniq.framework.illuminate.contracts.broadcasting.factory import Factory as BroadcastFactory
from pythoniq.framework.illuminate.contracts.broadcasting.shouldBroadcast import ShouldBroadcast
from pythoniq.framework.illuminate.contracts.queue.factory import Factory as QueueManager
from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.events.queuedClosure import QueuedClosure
from pythoniq.framework.illuminate.support.str import Str
from pythoniq.framework.illuminate.support.traits.macroable import Macroable
from pythoniq.framework.illuminate.contracts.queue.queue import Queue as QueueContract
from pythoniq.framework.illuminate.events.callQueuedListener import CallQueuedListener
from pythoniq.framework.illuminate.support.helpers import tap, _import_
from pythoniq.framework.illuminate.support.traits.reflectsClosures import ReflectsClosures


class Dispatcher(DispatcherContract, Macroable, ReflectsClosures):
    # The IoC container instance.
    _container: ContainerContract = None

    # An array of the types that have been resolved.
    _eventResolved: dict = {}

    # An array of the types that have been resolved.
    _listenerResolved: dict = {}

    # The registered event listeners.
    _listeners: dict = {}

    # The wildcard listeners.
    _wildcards: dict = {}

    # The cached wildcard listeners.
    _wildcardsCache: dict = {}

    # The queue resolver instance.
    _queueResolver: QueueManager = None

    # The signature to event mappings.
    _signatures: dict = {}

    def __init__(self, container: ContainerContract = None):
        self._container = container or Container()

    # Register an event listener with the dispatcher.
    def listen(self, events: callable | str | dict | list, listener: callable | str | dict | list = None) -> None:
        if isinstance(events, list):
            for event in events:
                self.listen(event, listener)

            return

        if Str.contains(events, '*'):
            self._setupWildcardListen(events, listener)
            return

        if events not in self._listeners:
            self._listeners[events] = []

        self._listeners[events].append(listener)

    def load(self, events: dict) -> None:
        for event, value in events.items():
            if 'signature' in value:
                self._signatures[value['signature']] = event

            if 'resolved' in value and value['resolved']:
                self._eventResolved[event] = value['resolved']

            for listener in value['listeners']:
                self.listen(event, listener)

    # Setup a wildcard listener callback.
    def _setupWildcardListen(self, event: str, listener: callable) -> None:
        self._wildcards[event].append(listener)
        self._wildcardsCache = {}

    # Determine if a given event has listeners.
    def hasListeners(self, eventName: str) -> bool:
        return eventName in self._listeners or eventName in self._wildcards or self.hasWildcardListeners(eventName)

    # Determine if the given event has any wildcard listeners.
    def hasWildcardListeners(self, eventName: str) -> bool:
        if not self._wildcards:
            return False

        if eventName in self._wildcardsCache:
            return True

        for key in self._wildcards:
            if self._patternMatch(key, eventName):
                self._wildcardsCache.append(eventName)
                return True

        return False

    # Register an event and payload to be fired later.
    def push(self, event: str, payload: dict = {}) -> None:
        self.listen(event + '_pushed', lambda: self.dispatch(event, payload))

    # Flush a set of pushed events.
    def flush(self, event: str) -> None:
        self.dispatch(event + '_pushed')

    # Register an event subscriber with the dispatcher.
    def subscribe(self, subscriber: object | str) -> None:
        subscriber = self._resolveSubscriber(subscriber)

        events = subscriber.subscribe(self)

        if isinstance(events, dict):
            for event, listeners in events.items():
                for listener in Arr.wrap(listeners):
                    if isinstance(listener, str) and hasattr(subscriber, listener):
                        self.listen(event, [subscriber.__class__.__name__, listener])

                        continue

                    self.listen(event, listener)

    # Resolve the subscriber instance.
    def _resolveSubscriber(self, subscriber: object | str) -> object:
        if isinstance(subscriber, str):
            return self._container.make(subscriber)

        return subscriber

    # Fire an event until the first non-null response is returned.
    def until(self, event: str | object, payload: dict = {}) -> None:
        return self.dispatch(event, payload, True)

    # Fire an event and call the listeners.
    def dispatch(self, event: str | object, payload: dict = {}, halt: bool = False) -> list | None:
        # When the given 'event' is actually an object we will assume it is an event
        # object and use the class as the event name and this event itself as the
        # payload to the handler, which makes object based events quite simple.
        [event, payload] = self._parseEventAndPayload(event, payload)

        if self._shouldBroadcast(payload):
            self._broadcastEvent(payload[0])

        responses = []
        for listener in self.getListeners(event):
            response = listener(event, payload)

            # If a response is returned from the listener and event halting is enabled
            # we will just return this response, and not call the rest of the event
            # listeners. Otherwise we will add the response on the response list.
            if halt and response is not None:
                return response

            # If a boolean false is returned from a listener, we will stop propagating
            # the event to any further listeners down in the chain, else we keep on
            # looping through the listeners and firing every one in our sequence.
            if responses is False:
                break

            responses.append(response)

        return halt and None or responses

    def _getModuleName(self, event: str) -> str | None:
        return self._signatures[event] or None

    # Parse the given event and payload and prepare them for dispatching.
    def _parseEventAndPayload(self, event: str | object, payload: dict) -> list:
        # Olay objesi ise event ismini al
        if hasattr(event, '__dict__') and event.__module__:
            className = Str.of(event.__module__).afterLast('.').studly().value()
            [payload, event] = [[event], event.__module__ + '.' + className]

        return [event, Arr.wrap(payload)]

    # Determine if the payload has a broadcastable event.
    def _shouldBroadcast(self, payload: dict) -> bool:
        return 0 in payload and isinstance(payload[0], ShouldBroadcast) and self._broadcastWhen(payload[0])

    # Check if the event should be broadcasted by the condition.
    def _broadcastWhen(self, event: ShouldBroadcast) -> bool:
        return hasattr(event, 'broadcastWhen') and event.broadcastWhen() or True

    # Broadcast the given event class.
    def _broadcastEvent(self, event: ShouldBroadcast) -> None:
        self._container.make(BroadcastFactory).queue(event)

    # Get all the listeners for a given event name.
    def getListeners(self, eventName: str) -> list:
        listeners = self._prepareListeners(eventName)
        if eventName in self._wildcardsCache:
            listeners += self._wildcardsCache[eventName]
        else:
            listeners += self.getWildcardListeners(eventName)

        return listeners

    # Get the wildcard listeners for the event.
    def getWildcardListeners(self, eventName: str) -> list:
        wilcard = []

        for key, listeners in self._wildcards.items():
            if Str.is_(key, eventName):
                for listener in listeners:
                    wilcard.append(self.makeListener(listener, True))

        self._wildcardsCache[eventName] = wilcard

        return self._wildcardsCache[eventName]

    # Prepare the listeners for a given event.
    def _prepareListeners(self, eventName: str) -> list:
        listeners = []

        if eventName in self._listeners:
            for listener in self._listeners[eventName]:
                listeners.append(self.makeListener(listener))

        return listeners

    # Register an event listener with the dispatcher.
    def makeListener(self, listener: callable | str | list | dict, wildcard: bool = False) -> callable:
        if isinstance(listener, str):
            return self.createClassListener(listener, wildcard)

        if isinstance(listener, list) and 0 in listener and isinstance(listener[0], str):
            return self.createClassListener(listener, wildcard)

        def fn(event, payload):
            if wildcard:
                return listener(event, *payload)

            return listener(*payload)

        return fn

    # Create a class based listener using the IoC container.
    def createClassListener(self, listener: str | list, wildcard: bool = False) -> callable:
        def fn(event, payload):
            if wildcard:
                return self._createClassCallable(listener)(event, *payload)

            callableCls = self._createClassCallable(listener)

            return callableCls(*payload)

        return fn

    # Create the class based event callable.
    def _createClassCallable(self, listener: str | list) -> callable:
        [cls, method] = isinstance(listener, list) and listener or self._parseClassCallable(listener)
        cls = self.listenerResolver(cls)

        if not hasattr(cls, method):
            method = '__call__'

        listener = cls()

        if self._handlerShouldBeQueued(cls):
            return self._createQueuedHandlerCallable(listener, method)

        if self._handlerShouldBeDispatchedAfterDatabaseTransactions(listener):
            return self._createCallbackForListenerRunningAfterCommits(listener, method)

        return lambda *args: getattr(listener, method)(*args)

    # Parse the class listener into class and method.
    def _parseClassCallable(self, listener: str) -> list:
        return Str.parseCallback(listener, 'handle')

    # Determine if the event handler class should be queued.
    def _handlerShouldBeQueued(self, listener) -> bool:

        if issubclass(listener, ShouldQueue):
            return True

        return False

    # Create a callable for putting an event handler on the queue.
    def _createQueuedHandlerCallable(self, cls: object, method: str) -> callable:
        def fn(*args):
            arguments = list(filter(lambda x: x, args))

            if self._handlerWantsToBeQueued(cls, arguments):
                return self._queueHandler(cls, method, arguments)

        return fn

    # Determine if the given event handler should be dispatched after all database transactions have committed.
    def _handlerShouldBeDispatchedAfterDatabaseTransactions(self, listener: any) -> bool:
        return True

    # Create a callable for dispatching a listener after database transactions.
    def _createCallbackForListenerRunningAfterCommits(self, listener: any, method: str) -> callable:
        return lambda *args: getattr(listener, method)(*args)

    # Determine if the event handler wants to be queued.
    def _handlerWantsToBeQueued(self, cls: object, arguments: list) -> bool:
        instance = cls

        if hasattr(instance, 'shouldQueue'):
            return instance.shouldQueue(arguments[0])

        return True

    # Queue the handler class.
    def _queueHandler(self, cls: object, method: str, arguments: list) -> None:
        [listener, job] = self._createListenerAndJob(cls, method, arguments)

        if hasattr(listener, 'viaConnection'):
            connectionName = len(arguments) > 0 and listener.viaConnection(arguments[0]) or listener.viaConnection()
        else:
            connectionName = hasattr(listener, 'connection') and listener.connection or None

        connection = self._resolveQueue().connection(connectionName)

        if hasattr(listener, 'viaQueue'):
            queue = len(arguments) > 0 and listener.viaQueue(arguments[0]) or listener.viaQueue()
        else:
            queue = hasattr(listener, 'queue') and listener.queue or None

        if hasattr(listener, 'delay'):
            connection.laterOn(queue, listener.delay, job)
        else:
            connection.pushOn(queue, job)

    # Create the listener and job for a queued listener.
    def _createListenerAndJob(self, listener, method, arguments) -> list:
        return [listener, self._propagateListenerOptions(listener, CallQueuedListener(listener, method, arguments))]

    # Propagate listener options to the job.
    def _propagateListenerOptions(self, listener: callable, job: CallQueuedListener) -> None:
        def fn(job: CallQueuedListener) -> None:
            data = job.data

            job.listener = listener

            job.afterCommit = hasattr(listener, 'afterCommit') and listener.afterCommit or None
            job.maxExceptions = hasattr(listener, 'maxExceptions') and listener.maxExceptions or None
            # job.shouldBeEncrypted = issubclass(listener, ShouldBeEncrypted)
            job.timeout = hasattr(listener, 'timeout') and listener.timeout or None
            job.tries = hasattr(listener, 'tries') and listener.tries or None

            job.backoff = None
            if hasattr(listener, 'getBackoff'):
                job.backoff = listener.getBackoff(*data)
            elif hasattr(listener, 'backoff'):
                job.backoff = listener.backoff

            job.retryUntil = None
            if hasattr(listener, 'getRetryUntil'):
                job.retryUntil = listener.getRetryUntil(*data)
            elif hasattr(listener, 'retryUntil'):
                job.retryUntil = listener.retryUntil

            job.middleware = []
            if hasattr(listener, 'getMiddleware'):
                job.middleware += listener.getMiddleware(*data)

            if hasattr(listener, 'middleware'):
                job.middleware += listener.middleware

            job.through(job.middleware)

        return tap(job, fn)

    # Remove a set of listeners from the dispatcher.
    def forget(self, eventName: str) -> None:
        if eventName.endswith('*'):
            self._wildcards.pop(eventName, None)
        else:
            self._listeners.pop(eventName, None)

        for key, listeners in self._wildcardsCache.items():
            if Str.is_(eventName, key):
                self._wildcardsCache.pop(key, None)

    # Forget all of the pushed listeners.
    def forgetPushed(self) -> None:
        for key, value in self._listeners.items():
            if key.endswith('_pushed'):
                self.forget(key)

    # Get the queue implementation from the resolver.
    def _resolveQueue(self) -> QueueManager:
        return self._queueResolver

    # Set the queue resolver implementation.
    def setQueueResolver(self, resolver: callable):
        self._queueResolver = resolver

        return self

    def signatureToEvent(self, signature: str) -> str:
        return self._signatures[signature] or None

    def eventResolver(self, event: str) -> callable:
        if event in self._eventResolved:
            return self._eventResolved[event]

        self._eventResolved[event] = _import_(event)

        if issubclass(self._eventResolved[event], QueuedClosure):
            self._eventResolved[event].resolve()

        return self._eventResolved[event]

    def listenerResolver(self, listener: str) -> callable:
        if listener in self._listenerResolved:
            return self._listenerResolved[listener]

        self._listenerResolved[listener] = _import_(listener)

        if issubclass(self._listenerResolved[listener], QueuedClosure):
            self._listenerResolved[listener].resolve()

        return self._listenerResolved[listener]

    # Gets the raw, unprepared listeners.
    def getRawListeners(self) -> dict:
        return self._listeners

    # Fire an event and call the listeners.
    def fire2(self, event: str | object, payload: list = []) -> list | None:
        from app.events.gsm.sms.send import Send

        return self.dispatch(Send(*payload))

    # Fire an event and call the listeners.
    def fire(self, event: str | object, payload: list = []) -> list | None:
        event = self.eventResolver(self.signatureToEvent(event))

        return self.dispatch(event(*payload))
