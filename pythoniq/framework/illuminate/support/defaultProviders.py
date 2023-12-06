class DefaultProviders:
    # The current providers.
    _providers: list = None

    # Create a new default provider collection.
    def __init__(self, providers: list = None) -> None:
        self._providers = providers or [
            # 'pythoniq.framework.illuminate.auth.authServiceProvider.AuthServiceProvider',
            # 'pythoniq.framework.illuminate.broadcasting.broadcastServiceProvider.BroadcastServiceProvider',
            'pythoniq.framework.illuminate.bus.busServiceProvider.BusServiceProvider',
            'pythoniq.framework.illuminate.cache.cacheServiceProvider.CacheServiceProvider',
            # 'pythoniq.framework.illuminate.foundation.providers.consoleSupportServiceProvider.ConsoleSupportServiceProvider',
            # 'pythoniq.framework.illuminate.cookie.cookieServiceProvider.CookieServiceProvider',
            # 'pythoniq.framework.illuminate.database.databaseServiceProvider.DatabaseServiceProvider',
            'pythoniq.framework.illuminate.encryption.encryptionServiceProvider.EncryptionServiceProvider',
            'pythoniq.framework.illuminate.filesystem.filesystemServiceProvider.FilesystemServiceProvider',
            # 'pythoniq.framework.illuminate.foundation.providers.foundationServiceProvider.FoundationServiceProvider',
            'pythoniq.framework.illuminate.hashing.hashServiceProvider.HashServiceProvider',
            # 'pythoniq.framework.illuminate.mail.mailServiceProvider.MailServiceProvider',
            # 'pythoniq.framework.illuminate.notifications.notificationServiceProvider.NotificationServiceProvider',
            # 'pythoniq.framework.illuminate.pagination.paginationServiceProvider.PaginationServiceProvider',
            'pythoniq.framework.illuminate.pipeline.pipelineServiceProvider.PipelineServiceProvider',
            'pythoniq.framework.illuminate.queue.queueServiceProvider.QueueServiceProvider',
            # 'pythoniq.framework.illuminate.redis.redisServiceProvider.RedisServiceProvider',
            # 'pythoniq.framework.illuminate.auth.passwords.passwordResetServiceProvider.PasswordResetServiceProvider',
            # 'pythoniq.framework.illuminate.session.sessionServiceProvider.SessionServiceProvider',
            # 'pythoniq.framework.illuminate.translation.translationServiceProvider.TranslationServiceProvider',
            # 'pythoniq.framework.illuminate.validation.validationServiceProvider.ValidationServiceProvider',
            # 'pythoniq.framework.illuminate.view.viewServiceProvider.ViewServiceProvider',
        ]

    # Merge the given providers into the provider collection.
    def merge(self, providers: list):
        self._providers += providers

        return DefaultProviders(self._providers)

    # Replace the given providers with other providers.
    def replace(self, providers: list):
        pass

    # Disable the given providers.
    def excepting(self, providers: list):
        pass

    # Convert the provider collection to an array.
    def toArray(self) -> list:
        return self._providers
