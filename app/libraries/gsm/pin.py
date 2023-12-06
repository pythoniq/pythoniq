from machine import Pin as PinMachine


class Pin:
    IN: int = PinMachine.IN
    OUT: int = PinMachine.OUT
    PULL_UP: int = PinMachine.PULL_UP
    PULL_DOWN: int = PinMachine.PULL_DOWN
    PULL_HOLD: int = PinMachine.PULL_HOLD
    IRQ_FALLING: int = PinMachine.IRQ_FALLING
    IRQ_RISING: int = PinMachine.IRQ_RISING

    def __init__(self):
        self._pins: dict[str] = {}

    def set(self, name: str, pin, mode: int = -1, pull: int = -1):
        self._pins[name] = PinMachine(pin, mode, pull)
        return self._pins[name]

    def get(self, name: str = None) -> dict | PinMachine:
        if name is None:
            return self.all()

        return self._pins[name]

    def irq(self, name: str, handler, trigger: int = -1):
        self.get(name).irq(handler=handler, trigger=trigger)

    def all(self) -> dict:
        return self._pins
