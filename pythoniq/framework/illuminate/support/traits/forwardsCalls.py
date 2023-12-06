class ForwardsCalls:
    def _forwardCallTo(self, object_: any, method: str, *parameters: list):
        try:
            return getattr(object_, method)(*parameters)
        except:
            self._throwBadMethodCallException(method)

    # Forward a method call to the given object, returning $this if the forwarded call returned itself.
    def _forwardDecoratedCallTo(self, object_, method, *parameters):
        result = self._forwardCallTo(object_, method, *parameters)

        return result == object_ and self or result

    @classmethod
    def _throwBadMethodCallException(cls, method) -> None:
        raise AttributeError('Call to undefined method %s::%s()' % (cls.__name__, method))
