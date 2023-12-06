from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from app.services.appService import AppService


class AppServiceProvider(ServiceProvider):
    def boot(self):
        appService = AppService(self._app)
        self._app.instance('appService', appService)
