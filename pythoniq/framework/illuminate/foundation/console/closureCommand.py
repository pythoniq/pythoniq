from pythoniq.framework.illuminate.console.command import Command
from pythoniq.framework.illuminate.contracts.console.input import Input as InputContract
from pythoniq.framework.illuminate.contracts.console.output import Output as OutputContract


class ClosureCommand(Command):
    def __init__(self, signature: str, callback: callable):
        self._signature = signature
        self._callback = callback

        super().__init__(signature)

    def _execute(self, input: InputContract, output: OutputContract):
        inputs = input.getArguments()
        inputs.update(input.getOptions())

        raise NotImplementedError

    def purpose(self, description: str):
        return self.describe(description)

    def describe(self, description: str):
        self.setDescription(description)

        return self
