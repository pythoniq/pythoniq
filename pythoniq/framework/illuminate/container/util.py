class Util:
    # If the given value is not an array and not null, wrap it in one.
    # From Arr::wrap() in Illuminate\Support.
    @staticmethod
    def arrayWrap(value):
        if value is None:
            return []
        return value if isinstance(value, list) else [value]

    # Return the default value of the given value.
    # From global value() helper in Illuminate\Support.
    @staticmethod
    def unwrapIfClosure(value, *parameters):
        if callable(value):
            return value(*parameters)
        return value

    # Get the class name of the given parameter's type, if possible.
    # From Reflector::getParameterClassName() in Illuminate\Support.
    @staticmethod
    def getParameterClassName(parameter):
        raise NotImplementedError('Base class Util does not implement getParameterClassName()')
