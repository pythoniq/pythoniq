from machine import Timer, Pin


class PowerOutageWatcherService:
    _counter: int = 0

    def __init__(self, cycle: int, pin: int):
        Timer(period=cycle, mode=Timer.PERIODIC, callback=self._counterAdd)

        power_failure = Pin(pin, Pin.IN, Pin.PULL_UP)
        power_failure.irq(handler=self._interrupt, trigger=Pin.IRQ_FALLING, hard=True)

    def _counterAdd(self, timer):
        self._counter += 1

    def _interrupt(self, pin):
        self._counter = 0

    def handle(self):
        if self._counter > 10:
            self._failure()
            return

        print("Power OK")

    def _failure(self):
        print("Power failure")
