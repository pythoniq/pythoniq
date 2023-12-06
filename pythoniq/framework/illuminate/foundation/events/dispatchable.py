from pythoniq.framework.illuminate.support.facades.app import App


class Dispatchable:
    # Dispatch the job with the given arguments.
    @classmethod
    def dispatch(cls, *arguments) -> None:
        App().event().dispatch(cls(*arguments))

    # Dispatch the job with the given arguments if the given truth test passes.
    @classmethod
    def dispatchIf(cls, boolean: bool, *arguments) -> None:
        if boolean:
            App().event().dispatch(cls(*arguments))

    # Dispatch the job with the given arguments unless the given truth test passes.
    @classmethod
    def dispatchUnless(cls, boolean: bool, *arguments) -> None:
        if not boolean:
            App().event().dispatch(cls(*arguments))
