class ReflectsClosures:
    # Get the class name of the first parameter of the given Closure.
    def _firstClosureParameterTypes(self, closure: callable) -> str:
        types = self._closureParameterTypes(closure)

        if not types:
            raise RuntimeError("The given Closure has no parameters.")

        if not types[0]:
            raise RuntimeError("The first parameter of the given Closure has no type hint.")

        return types[0]

    # Get the class names of the first parameter of the given Closure, including union types.
    def _firstParameterClassNames(self, closure: callable) -> list:
        raise NotImplementedError('ReflectionFunction')

    # Get the class names of the first parameter of the given Closure, including union types.
    def _closureParameterTypes(self, closure: callable) -> list:
        return closure
