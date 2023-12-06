from pythoniq.framework.illuminate.contracts.cache.repository import Repository as CacheContract


class UniqueLock:
    # The cache repository implementation.
    _cache: CacheContract = None

    # Create a new unique lock manager instance.
    def __init__(self, cache: CacheContract):
        self._cache = cache

    # Attempt to acquire a lock for the given job.
    def acquire(self, job: any):
        uniqueFor = hasattr(job, "uniqueFor") and job.uniqueFor() or (job.uniqueFor or 0)

        if hasattr(job, "uniqueVia"):
            cache = job.uniqueVia()
        else:
            cache = job.cache

        return bool(cache.lock(self._getKey(job), uniqueFor).get())

    # Release the lock for the given job.
    def release(self, job: any) -> None:
        cache = hasattr(job, "uniqueVia") and job.uniqueVia() or self._cache

        cache.lock(self._getKey(job)).forceRelease()

    # Generate the lock key for the given job.
    def _getKey(self, job: any) -> str:
        uniqueId = ''
        if hasattr(job, 'getUniqueId'):
            uniqueId = job.getUniqueId()
        elif hasattr(job, 'uniqueId'):
            uniqueId = job.uniqueId

        return 'laravel_unique_job:' + job.__class__.__name__ + uniqueId

