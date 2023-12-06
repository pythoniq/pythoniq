from pythoniq.framework.illuminate.bus.uniqueLock import UniqueLock
from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.queue.shouldBeUnique import ShouldBeUnique


class PendingDispatch:
    # The job.
    job: any = None

    # Indicates if the job should be dispatched immediately after sending the response.
    afterResponse_: bool = False

    # Create a new pending job dispatch.
    def __init__(self, job: any):
        self.job = job

    # Set the desired connection for the job.
    def onConnection(self, connection: str | None):
        self.job.onConnection(connection)

        return self

    # Set the desired queue for the job.
    def onQueue(self, queue: str | None):
        self.job.onQueue(queue)

        return self

    # Set the desired connection for the chain.
    def allOnConnection(self, connection: str | None):
        self.job.allOnConnection(connection)

        return self

    # Set the desired queue for the chain.
    def allOnQueue(self, queue: str | None):
        self.job.allOnQueue(queue)

        return self

    # Set the desired delay in seconds for the job.
    def delay(self, delay: int | None):
        self.job.delay(delay)

        return self

    # Indicate that the job should be dispatched after all database transactions have committed.
    def afterCommit(self):
        self.job.afterCommit()

        return self

    # Indicate that the job should not wait until database transactions have been committed before dispatching.
    def beforeCommit(self):
        self.job.beforeCommit()

        return self

    # Set the jobs that should run if this job is successful.
    def chain(self, jobs):
        self.job.chain(jobs)

        return self

    # Indicate that the job should be dispatched after the response is sent to the browser.
    def afterResponse(self):
        self.afterResponse_ = True

        return self

    # Determine if the job should be dispatched.
    def _shouldDispatch(self):
        if not isinstance(self.job, ShouldBeUnique):
            return True

        return UniqueLock(Container.getInstance().make(Cac))

    def fire(self):
        from pythoniq.framework.illuminate.support.facades.app import App
        if not self._shouldDispatch():
            return
        elif self.afterResponse_:
            App().make('bus').dispatchAfterResponse(self.job)
        else:
            App().make('bus').dispatch(self.job)

    def __del__(self):
        self.fire()
        pass
