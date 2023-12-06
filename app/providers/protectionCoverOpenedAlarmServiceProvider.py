from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from app.events.hardware.protectionCover.opened import Opened as ProtectionCoverOpenedEvent

from machine import Pin


class ProtectionCoverOpenedAlarmServiceProvider(ServiceProvider):
    def boot(self):
        pin = Pin(self._app.config().get('hardware.protectionCover.dejectPin'), Pin.IN)
        pin.irq(handler=self._eventFire, trigger=Pin.IRQ_RISING)

    def _eventFire(self, pin):
        ProtectionCoverOpenedEvent.dispatch()
