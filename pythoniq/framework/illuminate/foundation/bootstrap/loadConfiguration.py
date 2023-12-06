from lib.progressBar import progressBar
from pythoniq.framework.illuminate.foundation.application import Application
from pythoniq.framework.illuminate.config.configCache import ConfigCache
from pythoniq.framework.illuminate.config.repository import Repository
from pythoniq.framework.illuminate.filesystem.helpers import exists, files


class LoadConfiguration:
    # Bootstrap the given application.
    def bootstrap(self, app: Application):
        items = {}
        loadedFromCache = False

        # First we will see if we have a cache configuration file. If we do, we'll load
        # the configuration items from that file so that it is very quick. Otherwise
        # we will need to spin through every configuration file and load them all.
        cached = app.getCachedConfigPath()
        if exists(cached):
            try:
                items = ConfigCache.load(app.getCachedConfigPath())
                loadedFromCache = True
            except:
                print('Unable to load cached configuration file.')
                ConfigCache.clear(app.getCachedConfigPath())

        # Next we will spin through all of the configuration files in the configuration
        # directory and load each one into the repository. This will make all of the
        # options available to the developer for use in various parts of this app.
        config = Repository(items)
        app.instance('config', config)

        if not loadedFromCache:
            self._loadConfigurationFiles(app, config)
            ConfigCache.save(app.getCachedConfigPath(), config.all())

        # Finally, we will set the application's environment based on the configuration
        # values that were loaded. We will pass a callback which will be used to get
        # the environment in a web context where an "--env" switch is not present.
        app.detectEnvironment(lambda: config.get('app.env', 'production'))

    # Load the configuration items from all of the files.
    def _loadConfigurationFiles(self, app: Application, repository: Repository):
        files = self._getConfigurationFiles(app)

        if 'app' not in files:
            raise Exception('Unable to load the "app" configuration file.')

        index = 0
        for path, file in files.items():
            index += 1
            progressBar(index, len(files), 'import: ' + file + ' ' * 10)
            repository.set(path, __import__(file[:-3]).config())

        print('')

    # Get all of the configuration files for the application.
    def _getConfigurationFiles(self, app: Application) -> []:
        configPath = app.configPath()

        configFiles = {}
        for file in files(configPath):
            if file.endswith('.py'):
                configFiles[file[:-3]] = app.configPath(file)

        return configFiles

    # Get the configuration file nesting path.
    def _getNestedDirectory(self, file, configPath):
        return configPath + '/' + file
        # @todo - add support for nested directories
