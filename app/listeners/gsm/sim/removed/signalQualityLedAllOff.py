from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.support.facades.app import App
from app.libraries.gsm.events.sim.removed import Removed as Event


class SignalQualityLedAllOff(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        App().make('ioExpander.led').setPinState(4, 'low')
        App().make('ioExpander.led').setPinState(3, 'low')
        App().make('ioExpander.led').setPinState(2, 'low')
        App().make('ioExpander.led').setPinState(1, 'low')
        App().make('ioExpander.led').setPinState(0, 'low')
