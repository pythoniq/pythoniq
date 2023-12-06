from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.contracts.container.container import Container
from pythoniq.framework.illuminate.collections.arr import Arr
from pythoniq.framework.illuminate.events.jobQueued import JobQueued
from pythoniq.framework.illuminate.queue.callQueuedClosure import CallQueuedClosure
from pythoniq.framework.illuminate.queue.invalidPayloadException import InvalidPayloadException
from pythoniq.framework.illuminate.support.helpers import tap
from random import random
import json


class Queue(InteractsWithTime):
    # The IoC container instance.
    _container: Container = None

    # The connection name for the queue.
    _connectionName: str = None

    # Indicates that jobs should be dispatched after all database transactions have committed.
    _dispatchAfterCommit: bool = False

    # The create payload callbacks.
    _createPayloadCallbacks: list[callable] = []

    # Push a new job onto the queue.
    def pushOn(self, queue: str, job: str, data: dict = '') -> any:
        return self.push(job, data, queue)

    # Push a new job onto a specific queue after (n) seconds.
    def laterOn(self, queue: str, delay: int, job: str, data: dict = '') -> any:
        return self.later(delay, job, data, queue)

    # Push a raw of jobs onto the queue.
    def bulk(self, jobs: list, data: dict = '', queue: str = None) -> any:
        for job in jobs:
            self.push(job, data, queue)

    # Create a payload string from the given job and data.
    def _createPayload(self, job: str, queue: str = None, data: dict = '') -> dict:
        # if callable(job):
        #     job = CallQueuedClosure.create(job)

        return self._createPayloadArray(job, queue, data)

    # Create a payload array from the given job and data.
    def _createPayloadArray(self, job: str, queue: str, data: dict = '') -> dict:
        return (isinstance(job, object) and self._createObjectPayload(job, queue) or
                self._createStringPayload(job, queue, data))

    # Create a payload for an object-based queue handler.
    def _createObjectPayload(self, job: str, queue: str) -> dict:
        payload = self._withCreatePayloadHooks(queue, {
            'uuid': random(),
            'displayName': self._getDisplayName(job),
            'job': 'Illuminate\\Queue\\CallQueuedHandler@call',
            'maxTries': job.maxTries if hasattr(job, 'maxTries') else None,
            'maxExceptions': job.maxExceptions if hasattr(job, 'maxExceptions') else None,
            'failOnTimeout': job.failOnTimeout if hasattr(job, 'failOnTimeout') else None,
            'backoff': self.getJobBackoff(job),
            'timeout': job.timeout if hasattr(job, 'timeout') else None,
            'retryUntil': self.getJobExpiration(job),
            'data': {
                'commandName': job.__class__.__name__,
                'command': job
            }
        })

        return payload

    # Get the display name for the given job.
    def _getDisplayName(self, job: str) -> str:
        return hasattr(job, 'displayName') and job.displayName() or job.__class__.__name__

    # Get the backoff for an object-based queue handler.
    def getJobBackoff(self, job: any) -> any:
        if not hasattr(job, 'getBackoff') and not hasattr(job, 'backoff'):
            return

        backoff = None
        if hasattr(job, 'getBackoff'):
            backoff = job.getBackoff()
        else:
            backoff = job.backoff

        if backoff is None:
            return

        arr = Arr.wrap(backoff)
        arr = list(map(lambda backoff: self._secondsUntil(backoff), arr))
        return arr.join(',')

    # Get the expiration timestamp for an object-based queue handler.
    def getJobExpiration(self, job: any) -> any:
        if not hasattr(job, 'getRetryUntil') and not hasattr(job, 'retryUntil'):
            return

        if hasattr(job, 'getRetryUntil'):
            return job.getRetryUntil()
        else:
            return job.retryUntil

    # Determine if the job should be encrypted.
    def _jobShouldBeEncrypted(self, job: object) -> bool:
        return False
        if hasattr(job, 'shouldBeEncrypted'):
            return True

        return 'shouldBeEncrypted' in job and job.shouldBeEncrypted

    # Create a typical, string based queue payload array.
    def _createStringPayload(self, job: str, queue: str, data: dict) -> dict:
        return self._withCreatePayloadHooks(queue, {
            'uuid': random(),
            'displayName': isinstance(job, str) and job.split('@')[0] or None,
            'job': job,
            'maxTries': None,
            'maxExceptions': None,
            'failOnTimeout': False,
            'backoff': None,
            'timeout': None,
            'data': data
        })

    # Register a callback to be executed when creating job payloads.
    @classmethod
    def createPayloadUsing(cls, callback: callable) -> None:
        if callback is None:
            cls._createPayloadCallbacks = []
        else:
            cls._createPayloadCallbacks.append(callback)

    # Create the given payload using any registered payload hooks.
    def _withCreatePayloadHooks(self, queue: str, payload: dict) -> dict:
        if self._createPayloadCallbacks is not None:
            for callback in self._createPayloadCallbacks:
                payload.update(callback(self.getConnectionName()))

        return payload

    # Enqueue a job using the given callback.
    def _enqueueUsing(self, job: callable | str | object, payload: str, queue: str, delay: int,
                      callback: callable = None) -> any:
        def fn():
            return tap(callback(payload, queue, delay), lambda jobId: self._raiseJobQueuedEvent(jobId, job))

        if self._shouldDispatchAfterCommit(job) and self._container.bound('db.transactions'):
            return self._container.make('db.transactions').addCallback(fn)

        return tap(callback(payload, queue, delay), lambda jobId: self._raiseJobQueuedEvent(jobId, job))

    # Determine if the job should be dispatched after all database transactions have committed.
    def _shouldDispatchAfterCommit(self, job) -> bool:
        if not callable(job) and isinstance(job, object) and 'afterCommit' in job:
            return job.afterCommit

        if '_dispatchAfterCommit' in self:
            return self._dispatchAfterCommit

        return False

    # Raise the job queued event.
    def _raiseJobQueuedEvent(self, jobId: str | int | None, job: callable | str | object) -> None:
        if self._container.bound('events'):
            self._container.event().dispatch(JobQueued(self._connectionName, jobId, job))

    # Get the connection name for the queue.
    def getConnectionName(self) -> str:
        return self._connectionName

    # Set the connection name for the queue.
    def setConnectionName(self, name: str):
        self._connectionName = name

        return self

    # Get the container instance being used by the connection.
    def getContainer(self) -> Container:
        return self._container

    # Set the IoC container instance.
    def setContainer(self, container: Container) -> None:
        self._container = container
