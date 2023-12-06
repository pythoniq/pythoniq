from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from app.libraries.texas.tca6408a import TCA6408A


class IoExpanderServiceProvider(ServiceProvider):
    def boot(self):
        deviceAddress = self._app.config().get('hardware.ioExpander.led.deviceAddress')
        ioExpander = TCA6408A(self._app.make('i2c'), deviceAddress)

        ioExpander.setAllOutput()
        ioExpander.setAllPinState()

        self._app.instance('ioExpander.led', ioExpander)
