from pythoniq.framework.illuminate.support.higherOrderWhenProxy import HigherOrderWhenProxy


class Conditionable:
    # when(self, value: callable | None = None, callback: callable | None = None, default: callable | None = None):
    def when(self, *args):
        value = args[0]
        value = callable(value) and value(self) or value

        if len(args) == 0:
            return HigherOrderWhenProxy(self)

        if len(args) == 1:
            return HigherOrderWhenProxy(self).condition(value)

        if value:
            callback = args[1]
            return callback(self, value) or self

        default = args[2]
        if default:
            return default(self, value) or self

        return self

    # unless(self, value: callable | None = None, callback: callable | None = None, default: callable | None = None):
    def unless(self, *args):
        value = args[0]
        value = callable(value) and value(self) or value

        if len(args) == 0:
            return HigherOrderWhenProxy(self).negateConditionOnCapture()

        if len(args) == 1:
            return HigherOrderWhenProxy(self).condition(value)

        if value:
            callback = args[1]
            return callback(self, value) or self

        default = args[2]
        if default:
            return default(self, value) or self

        return self
