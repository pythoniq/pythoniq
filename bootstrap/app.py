from pythoniq.framework.illuminate.foundation.application import Application
from pythoniq.framework.illuminate.support.facades.facade import Facade

from app.kernel import Kernel as Kernel

import os

"""
|--------------------------------------------------------------------------
| Create The Application
|--------------------------------------------------------------------------
|
| The first thing we will do is create a new Pythoniq application instance
| which serves as the "glue" for all the components of Pythoniq, and is
| the IoC container for the system binding all of the various parts.
|
"""

app = Application(os.getcwd())
Facade.setFacadeApplication(app)

"""
|--------------------------------------------------------------------------
| Bind Important Interfaces
|--------------------------------------------------------------------------
|
| Next, we need to bind some important interfaces into the container so
| we will be able to resolve them when needed. The kernels serve the
| incoming requests to this application from both the web and CLI.
|
"""

app.singleton('kernel', Kernel)
