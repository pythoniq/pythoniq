class RegisterProviders:
    # Bootstrap the given application.
    def bootstrap(self, app) -> None:
        app.registerConfiguredProviders()
