class HigherOrderTapProxy:
    # The target being tapped.
    target = None

    # Create a new tap proxy instance.
    def __init__(self, target) -> None:
        self.target = target

    # Dynamically pass method calls to the target.
    def __getattr__(self, method):
        def _missing(*args):
            return getattr(self.target, method)(args)

        return _missing
