from pythoniq.framework.illuminate.events.eventCache import EventCache
from pythoniq.framework.illuminate.support.helpers import _import_
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider


class EventServiceProvider(ServiceProvider):
    # The event to listener mappings for the application.
    _listen = {
        # 'event.name': [
        #     'EventListener',
        # ],
    }

    # The subscribers to register.
    _subscribe = [
        # 'subscriber',
    ]

    # The model observers to register.
    _observers = {
        # 'user' => 'UserObserver',
    }

    # Register the application's event listeners.
    def register(self) -> None:
        def fn():
            self._app.event().load(self.getEvents())

            for subscriber in self._subscribe:
                self._app.event().subscribe(subscriber)

            for model, observer in self._observers.items():
                model.observe(observer)

        self.booting(fn)

    # Register any events for your application.
    def boot(self) -> None:
        pass

    # Get the events and handlers.
    def listens(self) -> dict:
        return self._listen

    # Get the discovered events and listeners for the application.
    def getEvents(self) -> dict:
        if self._app.eventsAreCached():
            try:
                cache = EventCache.load(self._app.getCachedEventsPath())
                return cache
            except:
                print('Unable to load cached events file.')
                EventCache.clear(self._app.getCachedEventsPath())

        events = {}
        tempModule = {}
        for event, listeners in self.listens().items():
            resolved = _import_(event)

            events.update({event: {
                'signature': resolved.getSignature(resolved),
                'resolved': None,
                'listeners': listeners,
            }})

            tempModule.update({event: resolved})

        EventCache.save(self._app.getCachedEventsPath(), events)

        for event, resolved in tempModule.items():
            events[event]['resolved'] = resolved

        del tempModule

        return events

    # Get the discovered events for the application.
    def _discoveredEvents(self) -> dict:
        return self.shouldDiscoverEvents() and self.discoverEvents() or {}

    # Determine if events and listeners should be automatically discovered.
    def shouldDiscoverEvents(self) -> bool:
        return False

    # Discover the events and listeners for the application.
    def discoverEvents(self) -> dict:
        raise NotImplementedError

    # Get the listener directories that should be used to discover events.
    def _discoverEventsWithin(self) -> list:
        return [
            self._app.path('listeners'),
        ]

    # Get the base path to be used during event discovery.
    def _eventDiscoveryBasePath(self) -> str:
        return self._app.basePath()
