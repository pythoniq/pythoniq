from pythoniq.framework.illuminate.contracts.foundation.application import Application
from pythoniq.framework.illuminate.support.env import Env
from lib.helpers import is_file


class LoadEnvironmentVariables:
    # Bootstrap the given application.
    def bootstrap(self, app: Application) -> None:
        if app.configurationIsCached():
            return

        self._checkForSpecificEnvironmentFile(app)

        try:
            self._createDotenv(app).safeLoad()
        except:
            self._writeErrorAndDie()

    # Detect if a custom environment file matching the APP_ENV exists.
    def _checkForSpecificEnvironmentFile(self, app: Application) -> None:
        environment = Env(app.environmentFilePath()).get('APP_ENV')

        if not environment:
            return

        self._setEnvironmentFilePath(app, app.environmentFile() + '.' + environment)

    # Load a custom environment file.
    def _setEnvironmentFilePath(self, app: Application, file: str) -> bool:
        envFile = app.environmentPath() + '/' + file
        if is_file(envFile):
            app.loadEnvironmentFrom(file)

            return True

        return False

    # Create a Dotenv instance.
    def _createDotenv(self, app: Application) -> Env:
        return Env().create(app.environmentPath(), app.environmentFile())

    # Write the error information to the screen and exit.
    def _writeErrorAndDie(self) -> None:
        print('The environment file is invalid!')

        import sys
        sys.exit(1)
