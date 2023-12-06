from app.libraries.gsm.gsmManager import GsmManager
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
import time


class GsmServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self):
        self._app.singleton('gsm', lambda app: GsmManager(app))

        self._app.singleton('gsm.uart', lambda app: app['gsm'].uart())

    def boot(self):
        self._app['gsm'].off()
        time.sleep_ms(100)
        
        self._app['gsm'].on()
