from pythoniq.framework.illuminate.contracts.pipeline.pipeline import Pipeline as PipelineContract
from pythoniq.framework.illuminate.contracts.container.container import Container


class Pipeline(PipelineContract):
    # The container implementation.
    _container: Container = None

    # The object being passed through the pipeline.
    _passable: any = None

    # The array of class pipes.
    _pipes: list = []

    # The method to call on each pipe.
    _method: str = 'handle'

    # Create a new class instance.
    def __init__(self, container: Container = None):
        self._container = container

    # Set the object being sent through the pipeline.
    def send(self, passable: any):
        self._passable = passable

        return self

    # Set the array of pipes.
    def through(self, pipes: list):
        self._pipes = pipes if isinstance(pipes, list) else list(pipes)

        return self

    # Push additional pipes onto the pipeline.
    def pipe(self, *pipes: list):
        self._pipes.extend(list(pipes))

        return self

    # Set the method to call on the pipes.
    def via(self, method: str):
        self._method = method

        return self

    # Run the pipeline with a final destination callback.
    def then(self, destination: callable) -> any:
        self.pipes().reverse()

        pipeline = self.array_reduce(self.pipes(), self._carry(), self._prepareDestination(destination))

        return pipeline(self._passable)

    # Run the pipeline and return the result.
    def thenReturn(self) -> any:
        return self.then(lambda passable: passable)

    # Get the final piece of the Closure onion.
    def _prepareDestination(self, destination: callable) -> callable:
        def fn(passable):
            try:
                return destination(passable)
            except Exception as e:
                return self._handleException(passable, e)

        return fn

    # Get a Closure that represents a slice of the application onion.
    def _carry(self) -> callable:
        def inner(stack, pipe):
            pipeLocal = pipe
            def inner_inner(passable):
                pipe = pipeLocal
                try:
                    if callable(pipe):
                        # If the pipe is a callable, then we will call it directly, but otherwise we
                        # will resolve the pipes out of the dependency container and call it with
                        # the appropriate method and arguments, returning the results back out.
                        return pipe(passable, stack)
                    elif not isinstance(pipe, object):
                        name, parameters = self._parsePipeString(pipe)

                        # If the pipe is a string we will parse the string and resolve the class out
                        # of the dependency injection container. We can then build a callable and
                        # execute the pipe function giving in the parameters that are required.
                        pipe = self._getContainer().make(name)

                        parameters = [passable, stack] + parameters
                    else:
                        # If the pipe is already an object we'll just make a callable and pass it to
                        # the pipe as-is. There is no need to do any extra parsing and formatting
                        # since the object we're given was already a fully instantiated object.
                        parameters = [passable, stack]

                    if hasattr(pipe, self._method):
                        carry = getattr(pipe, self._method)(*parameters)
                    else:
                        carry = pipe(*parameters)

                    return self._handleCarry(carry)
                except Exception as e:
                    return self._handleException(passable, e)

            return inner_inner

        return inner

    # Parse full pipe string to get name and parameters.
    def _parsePipeString(self, pipe: str) -> list:
        [name, parameters] = pipe.split(':', 2)
        if parameters is None:
            parameters = []

        if isinstance(parameters, str):
            parameters = parameters.split(',')

        return [name, parameters]

    # Get the array of configured pipes.
    def pipes(self) -> list:
        return self._pipes

    # Get the container instance.
    def _getContainer(self) -> Container:
        if self._container is None:
            raise Exception('A container instance has not been passed to the Pipeline.')

        return self._container

    # Set the container instance.
    def setContainer(self, container: Container):
        self._container = container

        return self

    # Handle the value returned from each pipe before passing it to the next.
    def _handleCarry(self, carry: any) -> any:
        return carry

    # Handle the given exception.
    def _handleException(self, passable: any, e: Exception) -> any:
        raise e

    def array_reduce(self, array: list, callback: callable, initial: any = None) -> any:
        result = initial

        for value in array:
            result = callback(result, value)

        return result
