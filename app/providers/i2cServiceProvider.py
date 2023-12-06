from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from machine import SoftI2C, Pin


class I2cServiceProvider(ServiceProvider):
    def boot(self):
        # _id = self._app.config().get('hardware.i2c.id')
        clock = self._app.config().get('hardware.i2c.clock')
        dataIo = self._app.config().get('hardware.i2c.dataIo')
        frequency = self._app.config().get('hardware.i2c.frequency')

        i2c = SoftI2C(scl=Pin(clock, Pin.PULL_UP), sda=Pin(dataIo, Pin.PULL_UP), freq=frequency)

        self._app.instance('i2c', i2c)

