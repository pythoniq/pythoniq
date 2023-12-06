from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.libraries.gsm.events.statusControl.signalQualityChanged import SignalQualityChanged as Event
from pythoniq.framework.illuminate.support.facades.app import App


class LedUpdate(ShouldQueue, InteractsWithQueue):
    queue: str = 'gsm'

    def handle(self, event: Event):
        rssi = event.getRssi()

        App().make('ioExpander.led').setPinState(4, 'low')
        App().make('ioExpander.led').setPinState(3, 'low')
        App().make('ioExpander.led').setPinState(2, 'low')
        App().make('ioExpander.led').setPinState(1, 'low')
        App().make('ioExpander.led').setPinState(0, 'low')

        if rssi == '99':
            return

        percent = round(int(rssi) * 100 / 31)

        if percent <= 20:
            App().make('ioExpander.led').setPinState(4, 'high')
        elif percent <= 40:
            App().make('ioExpander.led').setPinState(4, 'high')
            App().make('ioExpander.led').setPinState(3, 'high')
        elif percent <= 60:
            App().make('ioExpander.led').setPinState(4, 'high')
            App().make('ioExpander.led').setPinState(3, 'high')
            App().make('ioExpander.led').setPinState(2, 'high')
        elif percent <= 80:
            App().make('ioExpander.led').setPinState(4, 'high')
            App().make('ioExpander.led').setPinState(3, 'high')
            App().make('ioExpander.led').setPinState(2, 'high')
            App().make('ioExpander.led').setPinState(1, 'high')
        elif percent <= 100:
            App().make('ioExpander.led').setPinState(4, 'high')
            App().make('ioExpander.led').setPinState(3, 'high')
            App().make('ioExpander.led').setPinState(2, 'high')
            App().make('ioExpander.led').setPinState(1, 'high')
            App().make('ioExpander.led').setPinState(0, 'high')
