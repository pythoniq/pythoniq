from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from app.events.testEvent import TestEvent as Event


class Test(ShouldQueue, InteractsWithQueue):
    def handle(self, event: Event):
        print('Test listener')
        print(event, event.getArgs())
        
        0/0
    
    def failed(self, *args):
        pass