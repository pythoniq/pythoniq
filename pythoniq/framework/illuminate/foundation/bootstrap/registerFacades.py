from pythoniq.framework.illuminate.foundation.aliasLoader import AliasLoader
from pythoniq.framework.illuminate.support.facades.facade import Facade


class RegisterFacades:
    # Bootstrap the given application.
    def bootstrap(self, app) -> None:
        Facade.clearResolvedInstances()

        Facade.setFacadeApplication(app)

        AliasLoader.getInstance(app.make('config').get('app.aliases', {})).register()
