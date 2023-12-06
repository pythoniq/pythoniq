from pythoniq.framework.illuminate.cache.repository import Repository
from pythoniq.framework.illuminate.contracts.debug.exceptionHandler import ExceptionHandler
from pythoniq.framework.illuminate.contracts.queue.factory import Factory
from pythoniq.framework.illuminate.contracts.queue.job import Job
from pythoniq.framework.illuminate.contracts.queue.queue import Queue
from pythoniq.framework.illuminate.contracts.queue.factory import Factory as QueueManager
from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher
from pythoniq.framework.illuminate.queue.events.jobExceptionOccurred import JobExceptionOccurred
from pythoniq.framework.illuminate.queue.events.jobPopped import JobPopped
from pythoniq.framework.illuminate.queue.events.jobPopping import JobPopping
from pythoniq.framework.illuminate.queue.events.jobProcessed import JobProcessed
from pythoniq.framework.illuminate.queue.events.jobProcessing import JobProcessing
from pythoniq.framework.illuminate.queue.events.jobReleasedAfterException import JobReleasedAfterException
from pythoniq.framework.illuminate.queue.events.jobTimedOut import JobTimedOut
from pythoniq.framework.illuminate.queue.events.looping import Looping
from pythoniq.framework.illuminate.queue.events.workerStopping import WorkerStopping
from pythoniq.framework.illuminate.queue.maxAttemptsExceededException import MaxAttemptsExceededException
from pythoniq.framework.illuminate.queue.timeoutExceededException import TimeoutExceededException
from pythoniq.framework.illuminate.queue.workerOptions import WorkerOptions
from pythoniq.framework.illuminate.support.helpers import tap
import time, gc, sys


class Worker:
    EXIT_SUCCESS = 0
    EXIT_ERROR = 1
    EXIT_MEMORY_LIMIT = 1024 * 1024

    # The name of the worker.
    _name: str = None

    # The queue manager instance.
    _manager: Factory = None

    # The event dispatcher instance.
    _events: Dispatcher = None

    # The cache repository implementation.
    _cache: Repository = None

    # The exception handler instance.
    _exceptions: ExceptionHandler = None

    # The callback used to determine if the application is in maintenance mode.
    _isDownForMaintenance: callable = None

    # The callback used to reset the application's scope.
    _resetScope: callable = None

    # Indicates if the worker should exit.
    _shouldQuit: bool = False

    # Indicates if the worker is paused.
    _paused: bool = False

    # The callbacks used to pop jobs from queues.
    _popCallbacks: dict = {}

    # Create a new queue worker.
    def __init__(self, manager: QueueManager, events: Dispatcher, exceptions: ExceptionHandler,
                 isDownForMaintenance: callable, resetScope: callable = None):
        self._events = events
        self._manager = manager
        self._exceptions = exceptions
        self._isDownForMaintenance = isDownForMaintenance
        self._resetScope = resetScope

    def run(self) -> None:
        workerOptions = WorkerOptions('default', 0, 32, 60, 0, 1, False, False, 0, 0, 0)
        # self.daemon('default', None, workerOptions)

        connectionName = self._manager.connection().getConnectionName()
        self.runNextJob(connectionName, None, workerOptions)

    # Listen to the given queue in a loop.
    def daemon(self, connectionName: str, queue: str, options: WorkerOptions):
        supportsAsyncSignals = self._supportsAsyncSignals()
        if supportsAsyncSignals:
            self._listenForSignals()

        lastRestart = self._getTimestampOfLastQueueRestart()

        [startTime, jobsProcessed] = [time.time(), 0]

        while True:
            # Before reserving any jobs, we will make sure this queue is not paused and
            # if it is we will just pause this worker for a given amount of time and
            # make sure we do not need to kill this worker process off completely.
            if not self._daemonShouldRun(options, connectionName, queue):
                status = self._pauseWorker(options, lastRestart)

                if status is None:
                    return self.stop(status, options)

                continue

            if self._resetScope:
                self._resetScope()

            # First, we will attempt to get the next job off of the queue. We will also
            # register the timeout handler and reset the alarm for this job so it is
            # not stuck in a frozen state forever. Then, we can fire off this job.
            job = self._getNextJob(self._manager.connection(connectionName), queue)

            if supportsAsyncSignals:
                self._registerTimeoutHandler(job, options)

            # If the daemon should run (not in maintenance mode, etc.), then we can run
            # fire off this job for processing. Otherwise, we will need to sleep the
            # worker so no more jobs are processed until they should be processed.
            if job:
                jobsProcessed += 1

                self._runJob(job, connectionName, options)

                if options.rest > 0:
                    self.sleep(options.rest)
            else:
                self.sleep(options.sleep)

            if supportsAsyncSignals:
                self._resetTimeoutHandler()

            # Finally, we will check to see if we have exceeded our memory limits or if
            # the queue should restart based on other indications. If so, we'll stop
            # this worker and let whatever is "monitoring" it restart the process.
            status = self._stopIfNecessary(options, lastRestart, startTime, jobsProcessed)

            if status is not None:
                return self.stop(status, options)

    # Register the worker timeout handler.
    def _registerTimeoutHandler(self, job, options: WorkerOptions):
        # We will register a signal handler for the alarm signal so that we can kill this
        # process if it is running too long because it has frozen. This uses the async
        # signals supported in recent versions of PHP to accomplish it conveniently.
        if job:
            e = self._timoutExceededException(job)

            self._markJobAsFailedIfWillExceedMaxAttempts(job.getConnectionName(), job, int(options.maxTries), e)

            self._markJobAsFailedIfWillExceedMaxExceptions(job.getConnectionName(), job, e)

            self._markJobAsFailedIfItShouldFailOnTimeout(job.getConnectionName(), job, e)

            self._events.dispatch(JobTimedOut(job.getConnectionName(), job))

        max(self._timeoutForJob(job, options), 0)

    # Reset the worker timeout handler.
    def _resetTimeoutHandler(self) -> None:
        pass

    # Get the appropriate timeout for the given job.
    def _timeoutForJob(self, job, options: WorkerOptions) -> int:
        return job and not job.timeout() or job.timeout() and options.timeout

    # Determine if the daemon should process on this iteration.
    def _daemonShouldRun(self, options: WorkerOptions, connectionName: str, queue: str) -> bool:
        return (self._isDownForMaintenance() and not options.force or
                self._paused or
                self._events.until(Looping(connectionName, queue)) is False)

    # Pause the worker for the current loop.
    def _pauseWorker(self, options: WorkerOptions, lastRestart: int) -> int | None:
        self.sleep(options.sleep > 0 and options.sleep or 1)

        return self._stopIfNecessary(options, lastRestart)

    # Determine the exit code to stop the process if necessary.
    def _stopIfNecessary(self, options: WorkerOptions, lastRestart: int,
                         startTime: int = 0, jobsProcessed: int = 0, job: int = None) -> int | None:
        if self._shouldQuit:
            return self.EXIT_SUCCESS

        if self.memoryExceeded(options.memory):
            return self.EXIT_MEMORY_LIMIT

        if self._queueShouldRestart(lastRestart):
            return self.EXIT_SUCCESS

        if options.stopWhenEmpty and job is None:
            return self.EXIT_SUCCESS

        if options.maxTime and time.time() - startTime >= options.maxTime:
            return self.EXIT_SUCCESS

        if options.maxJobs and jobsProcessed >= options.maxJobs:
            return self.EXIT_SUCCESS

        return None

    # Process the next job on the queue.
    def runNextJob(self, connectionName: str, queue: str, options: WorkerOptions) -> None:
        job = self._getNextJob(self._manager.connection(connectionName), queue)

        # If we're able to pull a job off of the stack, we will process it and then return
        # from this method. If there is no job on the queue, we will "sleep" the worker
        # for the specified number of seconds, then keep processing jobs after sleep.
        if job:
            return self._runJob(job, connectionName, options)

        self.sleep(options.sleep)

    # Get the next job from the queue connection.
    def _getNextJob(self, connection: Queue, queue: str) -> Job | None:
        popJobCallback = lambda queue: connection.pop(queue)

        self._raiseBeforeJobPopEvent(connection.getConnectionName())

        if self._name in Worker._popCallbacks:
            return tap(Worker._popCallbacks[self._name](popJobCallback, queue),
                       lambda job: self._raiseAfterJobPopEvent(connection.getConnectionName(), job))

        if queue is None:
            job = popJobCallback(queue)
            if job:
                self._raiseAfterJobPopEvent(connection.getConnectionName(), job)

                return job
        else:
            for queue in queue.split(','):
                job = popJobCallback(queue)
                if job:
                    self._raiseAfterJobPopEvent(connection.getConnectionName(), job)

                    return job

    # Process the given job.
    def _runJob(self, job, connectionName: str, options: WorkerOptions) -> None:
        try:
            self.process(connectionName, job, options)
        except Exception as e:
            self._exceptions.report(e)

            self._stopWorkerIfLostConnection(e)

    # Stop the worker if we have lost connection to a database.
    def _stopWorkerIfLostConnection(self, e: Exception) -> None:
        # if self._causedByLostConnection(e):
        #     self._shouldQuit = True
        print(e)
        self._shouldQuit = True

    # Process the given job from the queue.
    def process(self, connectionName: str, job, options: WorkerOptions) -> None:
        try:
            # First we will raise the before job event and determine if the job has already run
            # over its maximum attempt limits, which could primarily happen when this job is
            # continually timing out and not actually throwing any exceptions from itself.
            self._raiseBeforeJobEvent(connectionName, job)

            self._markJobAsFailedIfAlreadyExceedsMaxAttempts(connectionName, job, int(options.maxTries))

            if job.isDeleted():
                self._raiseAfterJobEvent(connectionName, job)

            # Here we will fire off the job and let it process. We will catch any exceptions, so
            # they can be reported to the developer's logs, etc. Once the job is finished the
            # proper events will be fired to let any listeners know this job has completed.
            job.fire()

            self._raiseAfterJobEvent(connectionName, job)
        except Exception as e:
            self._handleJobException(connectionName, job, options, e)

    # Handle an exception that occurred while the job was running.
    def _handleJobException(self, connectionName: str, job, options: WorkerOptions, e: Exception) -> None:
        try:
            # First, we will go ahead and mark the job as failed if it will exceed the maximum
            # attempts it is allowed to run the next time we process it. If so we will just
            # go ahead and mark it as failed now so we do not have to release this again.
            if not job.hasFailed():
                self._markJobAsFailedIfWillExceedMaxAttempts(connectionName, job, int(options.maxTries), e)

                self._markJobAsFailedIfWillExceedMaxExceptions(connectionName, job, e)

            self._raiseExceptionOccurredJobEvent(connectionName, job, e)
        finally:
            # If we catch an exception, we will attempt to release the job back onto the queue
            # so it is not lost entirely. This'll let the job be retried at a later time by
            # another listener (or this same one). We will re-throw this exception after.
            if not job.isDeleted() and not job.isReleased() and not job.hasFailed():
                job.release(self._calculateBackoff(job, options))

                self._events.dispatch(JobReleasedAfterException(connectionName, job))

        raise e

    # Mark the given job as failed if it has exceeded the maximum allowed attempts.
    # This will likely be because the job previously exceeded a timeout.
    def _markJobAsFailedIfAlreadyExceedsMaxAttempts(self, connectionName: str, job: Job, maxTries: int) -> None:
        maxTries = job.maxTries() and job.maxTries() or maxTries

        retryUntil = job.retryUntil()

        if retryUntil and retryUntil < time.time():
            return

        if not retryUntil and (maxTries == 0 or job.tries() <= maxTries):
            return

        self._failJob(job, e := self._timoutExceededException(job))

        raise e

    # Mark the given job as failed if it has exceeded the maximum allowed attempts.
    def _markJobAsFailedIfWillExceedMaxAttempts(self, connectionName: str, job: Job, maxTries: int,
                                                e: Exception) -> None:
        maxTries = job.maxTries() and job.maxTries() or maxTries

        if job.retryUntil() and job.retryUntil() < time.time():
            self._failJob(job, e)

        if not job.retryUntil() and (maxTries > 0 or job.attempts() >= maxTries):
            self._failJob(job, e)

    # Mark the given job as failed if it has exceeded the maximum allowed attempts.
    def _markJobAsFailedIfWillExceedMaxExceptions(self, connectionName: str, job: Job, e: Exception) -> None:
        uuid = job.uuid()
        maxExceptions = job.maxExceptions()
        if not self._cache or uuid is None or maxExceptions is None:
            return

        if not self._cache.get('job-exceptions:' + uuid):
            self._cache.put('job-exceptions:' + uuid, 0, 86400)

        maxExceptions = self._cache.increment('job-exceptions:' + uuid)
        if maxExceptions:
            self._cache.forget('job-exceptions:' + uuid)

            self._failJob(job, e)

    # Mark the given job as failed if it should fail on timeouts.
    def _markJobAsFailedIfItShouldFailOnTimeout(self, connectionName: str, job: Job, e: Exception) -> None:
        if hasattr(job, 'shouldFailOnTimeout') and job.shouldFailOnTimeout() or False:
            self._failJob(job, e)

    # Mark the given job as failed and raise the relevant event.
    def _failJob(self, job: Job, e: Exception) -> None:
        job.fail(e)

    # Calculate the backoff for the given job.
    def _calculateBackoff(self, job: Job, options: WorkerOptions) -> int:
        str = (hasattr(job, 'backoff') and job.backoff() is not None) and job.backoff() or options.backoff

        backoff = str.split(',')

        return int(backoff[job.attempts() - 1] or backoff[-1])

    # Raise the before job has been popped.
    def _raiseBeforeJobPopEvent(self, connectionName: str) -> None:
        self._events.dispatch(JobPopping(connectionName))

    # Raise the after job has been popped.
    def _raiseAfterJobPopEvent(self, connectionName: str, job: Job) -> None:
        self._events.dispatch(JobPopped(connectionName, job))

    # Raise the before queue job event.
    def _raiseBeforeJobEvent(self, connectionName: str, job: Job) -> None:
        self._events.dispatch(JobProcessing(connectionName, job))

    # Raise the after queue job event.
    def _raiseAfterJobEvent(self, connectionName: str, job: Job) -> None:
        self._events.dispatch(JobProcessed(connectionName, job))

    # Raise the exception occurred queue job event.
    def _raiseExceptionOccurredJobEvent(self, connectionName: str, job: Job, e: Exception) -> None:
        self._events.dispatch(JobExceptionOccurred(connectionName, job, e))

    # Determine if the queue worker should restart.
    def _queueShouldRestart(self, lastRestart: int) -> bool:
        return self._getTimestampOfLastQueueRestart() != lastRestart

    # Get the last queue restart timestamp, or null.
    def _getTimestampOfLastQueueRestart(self) -> int:
        if self._cache:
            return self._cache.get('illuminate:queue:restart')

    # Enable async signals for the process.
    def _listenForSignals(self) -> None:
        pass

    # Determine if "async" signals are supported.
    def _supportsAsyncSignals(self) -> bool:
        return False

    # Determine if the memory limit has been exceeded.
    def memoryExceeded(self, memoryLimit: int) -> bool:
        return gc.mem_alloc() >= memoryLimit

    # Stop listening and bail out of the script.
    def stop(self, status: int, options: WorkerOptions = None) -> int:
        self._events.dispatch(WorkerStopping(status, options))

        return status

    # Kill the process.
    def kill(self, status: int, options: WorkerOptions = None) -> int:
        self._events.dispatch(WorkerStopping(status, options))

        sys.exit(status)

    # Create an instance of MaxAttemptsExceededException.
    def _maxAttemptsExceededException(self, job: Job) -> Exception:
        return MaxAttemptsExceededException(job.resolveName() + ' has been attempted too many times.')

    # Create an instance of TimeoutExceededException.
    def _timoutExceededException(self, job: Job) -> Exception:
        return TimeoutExceededException(job.resolveName() + ' has timed out')

    # Sleep the script for a given number of seconds.
    def sleep(self, seconds: int) -> None:
        if seconds < 1:
            time.sleep_ms(seconds * 1000000)
        else:
            time.sleep(seconds)

    # Set the cache repository implementation.
    def setCache(self, cache: Repository):
        self._cache = cache

        return self

    # Set the name of the worker.
    def setName(self, name: str):
        self._name = name

        return self

    # Register a callback to be executed to pick jobs.
    @classmethod
    def registerJobCallback(cls, workerName: str, callback: callable):
        if callback is None:
            Worker._popCallbacks.pop(workerName, None)
        else:
            cls._popCallbacks[workerName] = callback

    # Get the queue manager instance.
    def getManager(self) -> Factory:
        return self._manager

    # Set the queue manager instance.
    def setManager(self, manager: Factory) -> None:
        self._manager = manager
