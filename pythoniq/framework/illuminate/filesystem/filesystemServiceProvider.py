from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.filesystem.localFilesystem import LocalFilesystem
from pythoniq.framework.illuminate.filesystem.filesystemManager import FilesystemManager


class FilesystemServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self):
        self._app.singleton('files', lambda app: LocalFilesystem({'root': '/'}))

        self._app.singleton('filesystem', lambda app: FilesystemManager(app))

    # Get the services provided by the provider.
    def provides(self):
        return ['filesystem']
