from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from machine import UART, Pin


class UartServiceProvider(ServiceProvider, DeferrableProvider):
    def boot(self):
        self._meterUartInit()

    def _meterUartInit(self):
        _id = self._app.config().get('hardware.uart.meter.id')
        baudRate = self._app.config().get('hardware.uart.meter.baudRate')
        uart = UART(_id)
        uart.init(baudrate=baudRate, bits=7, parity=0, stop=1, timeout=1000)
        self._app.instance('uart.meter', uart)

        direction = self._app.config().get('hardware.uart.meter.rs485.directionPin')
        pin = Pin(direction, Pin.OUT)
        pin.off()
        self._app.instance('uart.meter.rs485.directionPin', pin)
