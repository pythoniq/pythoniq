from pythoniq.framework.illuminate.contracts.foundation.application import Application
from lib.printr import print_r


class AppService:
    def __init__(self, app: Application):
        self._app = app
#         self._gsm = self._app.make('gsm')

    def handle(self):
        print_r()
        print('System is ready.')

        while True:
            self._run()

    def _run(self):
#         self._gsm.check()

        self._app.worker().run()
