from pythoniq.framework.illuminate.cache.cacheManager import CacheManager
from pythoniq.framework.illuminate.cache.rateLimiter import RateLimiter
from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider


class CacheServiceProvider(DeferrableProvider, ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton('cache', lambda app: CacheManager(app))

        self._app.singleton('caches.tore', lambda app: app['cache'].driver())

        self._app.singleton(RateLimiter, lambda app: RateLimiter(app.cache().driver(app['config']['cache.limiter'])))

    # Get the services provided by the provider.
    def provides(self) -> list:
        return ['cache', 'cache.store', RateLimiter]
