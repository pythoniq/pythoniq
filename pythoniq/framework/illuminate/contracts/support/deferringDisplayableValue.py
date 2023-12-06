from pythoniq.framework.illuminate.contracts.support.htmlable import Htmlable


class DeferringDisplayableValue:
    # Resolve the displayable value that the class is deferring.
    def resolveDisplayableValue(self) -> Htmlable | str:
        pass
