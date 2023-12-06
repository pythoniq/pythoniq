from bootstrap.app import app
from pythoniq.framework.illuminate.contracts.console.kernel import Kernel as KernelContract

kernel = app.make(KernelContract)

kernel.handle('')

print(kernel.test)