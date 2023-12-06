from pythoniq.framework.illuminate.support.env import Env
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.str import Str


def config():
    return {
        # --------------------------------------------------------------------------
        # Default Cache Store
        # --------------------------------------------------------------------------
        #
        # This option controls the default cache connection that gets used while
        # using this caching library. This connection is used when another is
        # not explicitly specified when executing a given caching function.
        #
        'default': Env().get('CACHE_DRIVER', 'file'),

        # --------------------------------------------------------------------------
        # Cache Stores
        # --------------------------------------------------------------------------
        #
        # Here you may define all of the cache "stores" for your application as
        # well as their drivers. You may even define multiple stores for the
        # same cache driver to group types of items stored in your caches.
        #
        # Supported drivers: "array", "file", "null"
        #
        'stores': {
            'array': {
                'driver': 'array',
                'serialize': False,
            },

            'file': {
                'driver': 'file',
                'path': App().storagePath('framework/cache/data'),
                'lock_path': App().storagePath('framework/cache/data'),
            },

            'null': {
                'driver': 'null',
            },
        },
        # --------------------------------------------------------------------------
        # Cache Key Prefix
        # --------------------------------------------------------------------------
        #
        # When utilizing the APC, database, memcached, Redis, or DynamoDB cache
        # stores there might be other applications using the same cache. For
        # that reason, you may prefix every cache key to avoid collisions.
        #
        'prefix': Env().get('CACHE_PREFIX', Str.snake(Env().get('APP_NAME', 'pythoniq'), '_') + '_cache_'),
    }

