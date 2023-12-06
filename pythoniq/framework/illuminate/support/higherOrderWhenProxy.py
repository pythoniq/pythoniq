class HigherOrderWhenProxy:
    # The target being conditionally operated on.
    _target = None

    # The condition for proxying.
    _condition = None

    # Indicates whether the proxy has a condition.
    _hasCondition = False

    # Determine whether the condition should be negated.
    _negateConditionOnCapture: bool | None = None

    # Create a new proxy instance.
    def __init__(self, target) -> None:
        self._target = target

    # Set the condition on the proxy.
    def condition(self, condition: bool):
        self._condition = condition
        self._hasCondition = True

        return self

    # Indicate that the condition should be negated.
    def negateConditionOnCapture(self):
        self._negateConditionOnCapture = False

        return self

    # Proxy accessing an attribute onto the target.
    def __getitem__(self, key):
        if not self._condition:
            condition = self._target[key]
            return self.condition(self._negateConditionOnCapture or condition)

        return self._condition and self._target[key] or self._target
