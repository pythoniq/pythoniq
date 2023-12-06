from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.queue.job import Job as JobContract
from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.bus.queueable import Queueable


class CallQueuedListener(ShouldQueue, InteractsWithQueue, Queueable):
    # Create a new job instance.
    def __init__(self, cls: str, method: str, data: dict):
        # The listener class name.
        self.cls: str = cls

        # The listener class name.
        self.listener: str = None

        # The listener method.
        self.method: str = method

        # The data to be passed to the listener.
        self.data: dict = data

        # The number of times the job may be attempted.
        self.tries: int = None

        # The maximum number of exceptions allowed, regardless of attempts.
        self.maxExceptions: int = None

        # The number of seconds to wait before retrying a job that encountered an uncaught exception.
        self.backoff: int = None

        # The timestamp indicating when the job should timeout.
        self.retryUntil: int = None

        # The number of seconds the job can run before timing out.
        self.timeout: int = None

        # Indicates if the job should be encrypted.
        self.shouldBeEncrypted: int = False

    # Handle the queued job.
    def handle(self, container: Container) -> None:
        self._prepareData()

        handler = self._setJobInstanceIfNecessary(self._job, self.cls)
        
        print(handler, self.method, *self.data)

        getattr(handler, self.method)(*self.data)

    # Set the job instance of the given class if necessary.
    # @todo: This method is not implemented yet.
    def _setJobInstanceIfNecessary(self, job: JobContract, instance: object) -> object:
        if isinstance(instance, InteractsWithQueue):
            instance.setJob(job)

        return instance

    # Call the failed method on the job instance.
    # The event instance and the exception will be passed.
    def failed(self, e: Exception) -> None:
        self._prepareData()

        # handler = Container.getInstance().make(self.cls)
        handler = self.cls
        
        parameters = self.data + [e]

        if hasattr(handler, "failed"):
            handler.failed(*parameters)

    # Unserialize the data if needed.
    def _prepareData(self) -> None:
        if not isinstance(self.data, str):
            self.data = self.data

    # Get the display name for the queued job.
    def displayName(self) -> str:
        return self.cls.__class__.__module__

    # Prepare the instance for cloning.
    def __clone(self) -> None:
        self.data = map(lambda x: isinstance(x, object) and x or x.copy(), self.data)
