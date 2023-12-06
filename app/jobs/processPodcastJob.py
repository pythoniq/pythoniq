from pythoniq.framework.illuminate.bus.queueable import Queueable
from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.foundation.bus.dispatchable import Dispatchable
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue


class ProcessPodcastJob(ShouldQueue, Dispatchable, InteractsWithQueue, Queueable):
    queue: str = 'gsm'

    def __init__(self, *arguments):
        # Arguments to pass to the event handler.
        self._arguments: list = list(arguments)

    def handle(self, *args):
        print('ProcessPodcastJob')
        print(args)
