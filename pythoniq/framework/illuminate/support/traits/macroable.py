class Macroable:
    # The registered string macros.
    _macros = {}

    # Register a custom macro.
    def macro(self, name, macro) -> None:
        self._macros[name] = macro

    # Mix another object into the class.
    def mixin(self, mixin) -> None:
        raise NotImplementedError("Mixin not implemented.")

    # Checks if macro is registered.
    def hasMacro(self, name) -> bool:
        return name in self._macros

    # Flush the existing macros.
    def flushMacros(self) -> None:
        self._macros = {}

    # Dynamically handle calls to the class.
    def __call__(self, method, parameters):
        if not self.hasMacro(method):
            raise AttributeError('Method %s::%s does not exist.' % (self.__class__.__name__, parameters))
