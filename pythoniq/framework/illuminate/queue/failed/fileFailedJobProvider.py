from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.filesystem.helpers import exists
from pythoniq.framework.illuminate.queue.failed.failedJobProviderInterface import FailedJobProviderInterface
from pythoniq.framework.illuminate.queue.failed.prunableFailedJobProvider import PrunableFailedJobProvider

import json
import time


class FileFailedJobProvider(FailedJobProviderInterface, PrunableFailedJobProvider):
    # The file path where the failed job file should be stored.
    _path: str = None

    # The maximum number of failed jobs to retain.
    _limit: int = None

    # The lock provider resolver.
    _lockProviderResolver: callable = None

    # Create a new database failed job provider.
    def __init__(self, path: str, limit: int = 100, lockProviderResolver: callable = None) -> None:
        self._path = path
        self._limit = limit
        self._lockProviderResolver = lockProviderResolver

    # Log a failed job into storage.
    def log(self, connection: str, queue: str, payload: dict, exception: Exception) -> str | int | None:
        pass

    # Get a list of all of the failed jobs.
    def all(self) -> list:
        return self._read()

    # Get a single failed job.
    def find(self, id: str | int) -> dict | None:
        return Arr.first(self._read(), lambda job, key: job.id == id)

    # Delete a single failed job from storage.
    def forget(self, id: str | int) -> None:
        def fn():
            jobs = self._read()

            prunedJobs = list(filter(lambda job: job.id != id, jobs))

            return len(jobs) - len(prunedJobs)

        return self._lock(fn)

    # Flush all of the failed jobs from storage.
    def flush(self, hours: int | None = None) -> None:
        self.prune(time.time() - (hours * 3600) if hours else 0)

    # Prune all of the entries older than the given date.
    def prune(self, before: int) -> None:
        def fn():
            jobs = self._read()

            prunedJobs = list(filter(lambda job: job.failed_at_timestamp <= before, jobs))

            return len(jobs) - len(prunedJobs)

        return self._lock(fn)

    # Execute the given callback while holding a lock.
    def _lock(self, callback: callable) -> any:
        if not self._lockProviderResolver:
            return callback()

        return self._lockProviderResolver().lock('framework/failed_jobs', 5, callback)

    # Read the failed jobs file.
    def _read(self) -> list:
        if not exists(self._path):
            return []

        file = open(self._path, 'r')
        content = file.read()

        if not content:
            return []

        content = json.loads(content)
        return isinstance(content, list) and content or []

    # Write the given array of jobs to the failed jobs file.
    def _write(self, jobs: list) -> None:
        file = open(self._path, 'w')
        file.write(json.dumps(jobs))
        file.close()
