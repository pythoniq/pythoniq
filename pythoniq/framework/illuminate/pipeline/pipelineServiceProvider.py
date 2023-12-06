from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.contracts.pipeline.hub import Hub as HubContract
from pythoniq.framework.illuminate.pipeline.hub import Hub
from pythoniq.framework.illuminate.pipeline.pipeline import Pipeline


class PipelineServiceProvider(ServiceProvider, DeferrableProvider):
    # Register the service provider.
    def register(self) -> None:
        self._app.singleton(HubContract, Hub)

        self._app.bind('pipeline', lambda app: Pipeline(app))

    # Get the services provided by the provider.
    def provides(self) -> list:
        return [HubContract, 'pipeline']
