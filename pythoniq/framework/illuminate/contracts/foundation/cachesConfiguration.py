class CachesConfiguration:
    # Determine if the application configuration is cached.
    def configurationIsCached(self) -> bool:
        pass

    # Get the path to the configuration cache file.
    def getCachedConfigPath(self) -> str:
        pass

    # Get the path to the cached services.get file.
    def getCachedServicesPath(self) -> str:
        pass
