from pythoniq.framework.illuminate.container.boundMethod import BoundMethod
from pythoniq.framework.illuminate.container.contextualBindingBuilder import ContextualBindingBuilder
from pythoniq.framework.illuminate.container.rewindableGenerator import RewindableGenerator
from pythoniq.framework.illuminate.container.util import Util
from pythoniq.framework.illuminate.contracts.container.bindingResolutionException import BindingResolutionException
from pythoniq.framework.illuminate.contracts.container.circularDependencyException import CircularDependencyException
from pythoniq.framework.illuminate.contracts.container.container import Container as ContainerContract
from pythoniq.framework.illuminate.contracts.container.contextualBindingBuilder import \
    ContextualBindingBuilder as ContextualBindingBuilderContract
from pythoniq.framework.illuminate.support.helpers import _import_
from lib.helpers import end


class Container(ContainerContract):
    # The current globally available container (if any).
    instance_ = None

    # An array of the types that have been resolved.
    _resolved: list = []

    # The container's bindings.
    _bindings: dict = {}

    # The container's method bindings.
    _methodBindings: dict = {}

    # The container's shared instances.
    _instances: dict = {}

    # The registered type aliases.
    _scopedInstances: list = []

    # The registered type aliases.
    _aliases: dict = {}

    # The registered aliases keyed by the abstract name.
    _abstractAliases: dict = {}

    # The extension closures for services.
    _extenders: dict = {}

    # All of the registered tags.
    _tags: dict = {}

    # The stack of concretions currently being built.
    _buildStack: list = []

    # The parameter override stack.
    _with: list = []

    # The contextual binding map.
    contextual: dict = {}

    # All of the registered rebound callbacks.
    _reboundCallbacks: dict = {}

    # All of the global before resolving callbacks.
    _globalBeforeResolvingCallbacks: list = []

    # All of the global resolving callbacks.
    _globalResolvingCallbacks: list = []

    # All of the global after resolving callbacks.
    _globalAfterResolvingCallbacks: list = []

    # All of the resolving callbacks by class type.
    _beforeResolvingCallbacks: dict = {}

    # All of the resolving callbacks by class type.
    _resolvingCallbacks: dict = {}

    # All of the after resolving callbacks by class type.
    _afterResolvingCallbacks: dict = {}

    # Define a contextual binding.
    def when(self, concrete: str | list) -> ContextualBindingBuilderContract:
        if isinstance(concrete, str):
            concrete = [concrete]

        aliases = []

        for c in concrete:
            aliases.append(self.getAlias(c))

        return ContextualBindingBuilder(self, aliases)

    # Determine if the given abstract type has been bound.
    def bound(self, abstract: str) -> bool:
        return abstract in self._bindings or abstract in self._instances or self.isAlias(abstract)

    #
    def has(self, id: str) -> bool:
        return self.bound(id)

    # Determine if the given abstract type has been resolved.
    def resolved(self, abstract: str) -> bool:
        if self.isAlias(abstract):
            abstract = self.getAlias(abstract)

        return abstract in self._resolved or abstract in self._instances

    # Determine if a given type is shared.
    def isShared(self, abstract: str) -> bool:
        return abstract in self._instances or (abstract in self._bindings and
                                               'shared' in self._bindings[abstract] and self._bindings[abstract][
                                                   'shared'] is True)

    # Determine if a given string is an alias.
    def isAlias(self, name: str) -> bool:
        return name in self._aliases

    # Register a binding with the container.
    def bind(self, abstract: str | callable, concrete: callable | str | None = None, shared: bool = False) -> None:
        self._dropStaleInstances(abstract)

        # If no concrete type was given, we will simply set the concrete type to the
        # abstract type. After that, the concrete type to be registered as shared
        # without being forced to state their classes in both of the parameters.
        if concrete is None:
            concrete = abstract

        # If the factory is not a Closure, it means it is just a class name which is
        # bound into this container to the abstract type and we will just wrap it
        # up inside its own Closure to give us more convenience when extending.
        if not callable(concrete):
            if not isinstance(concrete, str):
                raise TypeError(
                    self.__class__.__name__ + "::bind(): Argument #2 (concrete) must be of type Callable|str|None")

            concrete = self.getClosure(abstract, concrete)

        self._bindings[abstract] = {'concrete': concrete, 'shared': shared}

        # If the abstract type was already resolved in this container we'll fire the
        # rebound listener so that any objects which have already gotten resolved
        # can have their copy of the object updated via the listener callbacks.
        if self.resolved(abstract):
            self._rebound(abstract)

    # Get the Closure to be used when building a type.
    def getClosure(self, abstract: str, concrete: str) -> callable:
        def fn(container: ContainerContract, parameters: list = []):
            if abstract == concrete:
                return container.build(concrete)

            return container._resolve(concrete, parameters, raiseEvents=False)

        return fn

    # Determine if the container has a method binding.
    def hasMethodBinding(self, method: str) -> bool:
        return method in self._methodBindings

    # Bind a callback to resolve with Container.call.
    def bindMethod(self, method: list | str, callback: callable) -> None:
        self._methodBindings[self.parseBindMethod(method)] = callback

    # Get the method to be bound. Parse an array or string. @todo checking
    def parseBindMethod(self, method: list | str) -> str:
        if isinstance(method, dict):
            return method[0] + '@' + method[1]

        return method

    # Get the method binding for the given method.
    def callMethodBinding(self, method: str, instance) -> any:
        return self._methodBindings[method](instance, self)

    # Add a contextual binding to the container.
    def addContextualBinding(self, concrete: str, abstract: str, implementation: callable | str) -> None:
        self.contextual[concrete][self.getAlias(abstract)] = implementation

    # Register a binding if it hasn't already been registered.
    def bindIf(self, abstract: str, concrete: callable | str | None = None, shared: bool = False) -> None:
        if self.bound(abstract):
            self.bind(abstract, concrete, shared)

    # Register a shared binding in the container.
    def singleton(self, abstract: str | callable, concrete: callable | str | None = None) -> None:
        self.bind(abstract, concrete, True)

    # Register a shared binding if it hasn't already been registered.
    def singletonIf(self, abstract: str, concrete: callable | str | None = None) -> None:
        if self.bound(abstract):
            self.singleton(abstract, concrete)

    # Register a scoped binding in the container.
    def scoped(self, abstract: str, concrete: callable | str | None = None) -> None:
        if self.bound(abstract):
            self.scoped(abstract, concrete)

    # Register a scoped binding if it hasn't already been registered.
    def scopedIf(self, abstract: str, concrete: callable | str | None = None) -> None:
        if self.bound(abstract):
            self.scoped(abstract, concrete)

    # 'Extend' an abstract type in the container.
    def extend(self, abstract: str, closure: callable) -> None:
        abstract = self.getAlias(abstract)

        if abstract in self._instances:
            self._instances[abstract] = closure(self._instances[abstract], self)
        else:
            self._extenders[abstract].append(closure)

            if self.resolved(abstract):
                self._rebound(abstract)

    # Register an existing instance as shared in the container.
    def instance(self, abstract: str | callable, instance) -> any:
        self.removeAbstractAlias(abstract)

        isBound = self.bound(abstract)

        self._aliases.pop(abstract, None)

        self._instances[abstract] = instance

        if isBound:
            self._rebound(abstract)

        return instance

    # Remove an alias from the contextual binding alias cache.
    def removeAbstractAlias(self, searched: str) -> None:
        if searched not in self._aliases:
            return

        for abstract, aliases in self._abstractAliases.items():
            for index, alias in aliases:
                if alias == searched:
                    del self._abstractAliases[abstract][index]

    # Assign a set of tags to a given binding.
    def tag(self, tags: list | str, abstracts: list | str, *args) -> None:
        if not isinstance(tags, list):
            tags = [tags]
        tags = tags + list(args)

        for tag in tags:
            if tag not in self._tags:
                self._tags[tag] = []

            for abstract in Util.arrayWrap(abstracts):
                self._tags[tag].append(abstract)

    # Resolve all of the bindings for a given tag.
    def tagged(self, tag: str) -> RewindableGenerator:
        if tag not in self._tags:
            return RewindableGenerator([], 0)

        def fn():
            for abstract in self._tags[tag]:
                yield self.make(abstract)

        return RewindableGenerator(fn, len(self._tags[tag]))

    # Alias a type to a different name.
    def alias(self, abstract: str, alias: str) -> None:
        if alias == abstract:
            raise Exception('[{' + abstract + ']} is aliased to itself.')

        self._aliases[alias] = abstract

        if abstract not in self._abstractAliases:
            self._abstractAliases[abstract] = []

        self._abstractAliases[abstract].append(alias)

    # Bind a new callback to an abstract's rebind event.
    def rebinding(self, abstract: str, callback: callable) -> any:
        abstract = self.getAlias(abstract)

        if abstract not in self._reboundCallbacks:
            self._reboundCallbacks[abstract] = []

        self._reboundCallbacks[abstract].append(callback)

        if self.bound(abstract):
            return self.make(abstract)

    # Refresh an instance on the given target and method.
    def refresh(self, abstract: str, target: any, method: str) -> any:
        return self.rebinding(abstract, lambda app, instance: getattr(target, method)(instance))

    # Fire the "rebound" callbacks for the given abstract type.
    def _rebound(self, abstract: str) -> None:
        instance = self.make(abstract)

        for callback in self._getReboundCallbacks(abstract):
            callback(self, instance)

    # Get the rebound callbacks for a given type.
    def _getReboundCallbacks(self, abstract) -> list:
        if abstract in self._reboundCallbacks:
            return self._reboundCallbacks[abstract]

        return []

    # Wrap the given closure such that its dependencies will be injected when executed.
    def wrap(self, callback: callable, parameters: list = []) -> callable:
        def fn(app: ContainerContract):
            return app.call(callback, parameters)

        return fn

    # Call the given Closure / class@method and inject its dependencies.
    def call(self, callback: str | callable | list, parameters: list = [], defaultMethod: str | None = None) -> any:
        pushedToBuildStack = False

        if isinstance(callback, list):
            className = (isinstance(callback[0], str) and callback[0] or callback[0].__class__.__name__)
            if className not in self._buildStack:
                self._buildStack.append(className)
                pushedToBuildStack = True
                
        result = BoundMethod.call(self, callback, parameters, defaultMethod)

        if pushedToBuildStack:
            self._buildStack.pop()

        return result

    # Get the class name for the given callback, if one can be determined.
    def _getClassForCallable(self, callback: callable) -> str | None:
        if not isinstance(callback, list):
            return None

        return isinstance(callback[0], str) and callback[0] or callback[0].__class__.__name__

    # Get a closure to resolve the given type from the container.
    def factory(self, abstract: str) -> callable:
        return lambda *args: self.make(abstract, list(args))

    # An alias function name for make().
    def makeWith(self, abstract: str, parameters: list) -> any:
        return self.make(abstract, parameters)

    # Resolve the given type from the container.
    def make(self, abstract: str | callable, parameters: list = []) -> any:
        return self._resolve(abstract, parameters)

    #
    def get(self, id: str) -> any:
        try:
            return self._resolve(id)
        except Exception as e:
            if self.has(id) or isinstance(e, CircularDependencyException):
                raise e

        raise Exception('Unable to resolve dependency [' + id + ']')

    # Resolve the given type from the container.
    def _resolve(self, abstract: str | callable, parameters: list = [], raiseEvents: bool = True) -> any:
        abstract = self.getAlias(abstract)

        # First we'll fire any event handlers which handle the "before" resolving of
        # specific types. This gives some hooks the chance to add various extends
        # calls to change the resolution of objects that they're interested in.
        if raiseEvents:
            self._fireBeforeResolvingCallbacks(abstract, parameters)

        concrete = self._getContextualConcrete(abstract)

        needsContextualBuild = len(parameters) > 0 or concrete is not None

        # If an instance of the type is currently being managed as a singleton we'll
        # just return an existing instance instead of instantiating new instances
        # so the developer can keep using the same objects instance every time.
        if abstract in self._instances and not needsContextualBuild:
            return self._instances[abstract]

        self._with.append(parameters)

        if concrete is None:
            concrete = self._getConcrete(abstract)

        # We're ready to instantiate an instance of the concrete type registered for
        # the binding. This will instantiate the types, as well as resolve any of
        # its "nested" dependencies recursively until all have gotten resolved.
        if self._isBuildable(concrete, abstract):
            object_ = self.build(concrete)
        else:
            object_ = self.make(concrete)

        # If we defined any extenders for this type, we'll need to spin through them
        # and apply them to the object being built. This allows for the extension
        # of services, such as changing configuration or decorating the object.
        for extender in self._getExtenders(abstract):
            object_ = extender(object_, self)

        # If the requested type is registered as a singleton we'll want to cache off
        # the instances in "memory" so we can return it later without creating an
        # entirely new instance of an object on each subsequent request for it.
        if self.isShared(abstract) and not needsContextualBuild:
            self._instances[abstract] = object_

        if raiseEvents:
            self._fireResolvingCallbacks(abstract, object_)

        # Before returning, we will also set the resolved flag to "true" and pop off
        # the parameter overrides for this build. After those two things are done
        # we will be ready to return back the fully constructed class instance.
        self._resolved.append(abstract)

        self._with.pop()

        return object_

    # Get the concrete type for a given abstract.
    def _getConcrete(self, abstract: str | callable) -> any:
        # If we don't have a registered resolver or concrete for the type, we'll just
        # assume each type is a concrete name and will attempt to resolve it as is
        # since the container should be able to resolve concretes automatically.
        if abstract in self._bindings:
            return self._bindings[abstract]['concrete']

        return abstract

    # Get the contextual concrete binding for the given abstract.
    def _getContextualConcrete(self, abstract: str | callable) -> callable | str | list | dict | None:
        binding = self._findInContextualBindings(abstract)
        if binding is not None:
            return binding

        # Next we need to see if a contextual binding might be bound under an alias of the
        # given abstract type. So, we will need to check if any aliases exist with this
        # type and then spin through them and check for contextual bindings on these.
        if abstract not in self._abstractAliases:
            return

        for alias in self._abstractAliases[abstract]:
            binding = self._findInContextualBindings(alias)
            if binding is not None:
                return binding

    # Find the concrete binding for the given abstract in the contextual binding array.
    def _findInContextualBindings(self, abstract: str | callable) -> callable | str | None:
        if len(self._buildStack) == 0:
            return

        return self.contextual[end(self._buildStack)][abstract] or None

    # Determine if the given concrete is buildable.
    def _isBuildable(self, concrete, abstract: str) -> bool:
        return concrete == abstract or callable(concrete)

    # Instantiate a concrete instance of the given type.
    def build(self, concrete: callable | str) -> any:
        # If the concrete type is actually a Closure, we will just execute it and
        # hand back the results of the functions, which allows functions to be
        # used as resolvers for more fine-tuned resolution of these objects.
        if callable(concrete):
            return concrete(self, *self._getLastParameterOverride())

        try:
            raise NotImplementedError
            module = _import_(concrete)
        except Exception as e:
            raise BindingResolutionException(f'Target {concrete} is not instantiable.', 0, e)

        # If the type is not instantiable, the developer is attempting to resolve
        # an abstract type such as an Interface or Abstract Class and there is
        # no binding registered for the abstractions so we need to bail out.
        if not hasattr(module, '__dict__') or not module.__dict__.get('__module__'):
            self._notInstantiable(concrete)
            return

        self._buildStack.append(concrete)

        # If there are no constructors, that means there are no dependencies then
        # we can just resolve the instances of the objects right away, without
        # resolving any other types or dependencies out of these containers.
        if not hasattr(module, '__init__'):
            self._buildStack.pop()

            return module()

        self._buildStack.pop()

        return module(*self._getLastParameterOverride())

    # Resolve all of the dependencies from the ReflectionParameters.
    def _resolveDependencies(self, dependencies: list) -> list:
        results = []

        for dependency in dependencies:
            # If the dependency has an override for this particular build we will use
            # that instead as the value. Otherwise, we will continue with this run
            # of resolutions and let reflection attempt to determine the result.
            if self._hasParameterOverride(dependency):
                results.append(self._getParameterOverride(dependency))
                continue

            # If the class is null, it means the dependency is a string or some other
            # primitive type which we can not resolve since it is not a class and
            # we will just bomb out with an error since we have no-where to go.
            if Util.getParameterClassName(dependency) is not None:
                result = self._resolvePrimitive(dependency)
            else:
                result = self._resolveClass(dependency)

            if dependency.isVariadic():
                results = results + result
            else:
                results.append(result)

        return results

    # Determine if the given dependency has a parameter override.
    def _hasParameterOverride(self, dependency: any) -> bool:
        return dependency.name() in self._getLastParameterOverride().keys()

    # Get a parameter override for a dependency.
    def _getParameterOverride(self, dependency: any) -> any:
        return self._getLastParameterOverride()[dependency.name]

    # Get the last parameter override.
    def _getLastParameterOverride(self) -> dict:
        if len(self._with):
            return self._with[-1]

        return {}

    # Resolve a non-class hinted primitive dependency.
    def _resolvePrimitive(self, parameter: any) -> any:
        concrete = self._getContextualConcrete(parameter.getName())
        if concrete is not None:
            return Util.unwrapIfClosure(concrete, self)

        if parameter.isDefaultValueAvailable():
            return parameter.getDefaultValue()

        if parameter.isVariadic():
            return []

        self._unresolvablePrimitive(parameter)

    # Resolve a class based dependency from the container.
    def _resolveClass(self, parameter: any) -> any:
        try:
            if parameter.isVariadic():
                return self._resolveVariadicClass(parameter)
            else:
                return self.make(Util.getParameterClassName(parameter))

        # If we can not resolve the class instance, we will check to see if the value
        # is optional, and if it is we will return the optional parameter value as
        # the value of the dependency, similarly to how we do this with scalars.
        except Exception as e:
            if parameter.isDefaultValueAvailable():
                self._with.pop()
                return parameter.getDefaultValue()

            if parameter.isVariadic():
                self._with.pop()
                return []

            raise e

    # Resolve a class based variadic dependency from the container.
    def _resolveVariadicClass(self, parameter: any) -> list:
        className = Util.getParameterClassName(parameter)
        abstract = self.getAlias(className)

        concrete = self._getContextualConcrete(abstract)
        if isinstance(concrete, list) or isinstance(concrete, dict):
            return self.make(className)

        return list(filter(lambda abstract: self._resolve(abstract), concrete))

    # Throw an exception that the concrete is not instantiable.
    def _notInstantiable(self, concrete: any) -> any:
        if len(self._buildStack):
            previous = ' '.join(self._buildStack)

            message = 'Target [' + concrete + '] is not instantiable while building [' + previous + '].'
        else:
            message = 'Target [' + concrete + '] is not instantiable.'

        raise BindingResolutionException(message)

    # Throw an exception for an unresolvable primitive.
    def _unresolvablePrimitive(self, parameter: any) -> None:
        message = "Unresolvable dependency resolving [$parameter] in class {$self._buildStack[-1]}"

        raise BindingResolutionException(message)

    # Register a new before resolving callback for all types.
    def beforeResolving(self, abstract: str | callable, callback: callable | None = None) -> None:
        if isinstance(abstract, str):
            abstract = self.getAlias(abstract)

        if callable(abstract) and callback is None:
            self._globalResolvingCallbacks.append(abstract)
        else:
            self._resolvingCallbacks[abstract].append(callback)

    # Register a new resolving callback.
    def resolving(self, abstract: str | callable, callback: callable | None = None) -> None:
        if isinstance(abstract, str):
            abstract = self.getAlias(abstract)

        if callback is None and callable(abstract):
            self._globalResolvingCallbacks.append(abstract)
        else:
            self._resolvingCallbacks[abstract].append(callback)

    # Register a new after resolving callback for all types.
    def afterResolving(self, abstract: str | callable, callback: callable | None = None) -> None:
        if isinstance(abstract, str):
            abstract = self.getAlias(abstract)

        if callback is None and callable(abstract):
            self._globalAfterResolvingCallbacks.append(abstract)
        else:
            self._afterResolvingCallbacks[abstract].append(callback)

    # Fire all of the before resolving callbacks.
    def _fireBeforeResolvingCallbacks(self, abstract: str, parameters: any) -> None:
        self._fireBeforeCallbackArray(abstract, parameters, self._globalBeforeResolvingCallbacks)

        for key, callback in self._beforeResolvingCallbacks.items():
            if type == abstract or issubclass(abstract, key):
                self._fireBeforeCallbackArray(abstract, parameters, callback)

    # Fire an array of callbacks with an object.
    def _fireBeforeCallbackArray(self, abstract: str, parameters: list, callbacks: list) -> None:
        for callback in callbacks:
            callback(abstract, parameters, self)

    # Fire all of the resolving callbacks.
    def _fireResolvingCallbacks(self, abstract: str, object_: any) -> None:
        self._fireCallbackArray(object_, self._globalResolvingCallbacks)

        self._fireCallbackArray(object_, self._getCallbacksForType(abstract, object_, self._resolvingCallbacks))

        self._fireAfterResolvingCallbacks(abstract, object_)

    # Fire all of the after resolving callbacks.
    def _fireAfterResolvingCallbacks(self, abstract: str, object_: any) -> None:
        self._fireCallbackArray(object_, self._globalAfterResolvingCallbacks)

        self._fireCallbackArray(object_, self._getCallbacksForType(abstract, object_, self._afterResolvingCallbacks))

    # Get all callbacks for a given type.
    def _getCallbacksForType(self, abstract: str, object_: callable, callbacksPerType: dict) -> list:
        results = []

        for type_, callbacks in callbacksPerType.items():
            if type_ == abstract or issubclass(object_, type_):
                results += callbacks

        return results

    # Fire an array of callbacks with an object.
    def _fireCallbackArray(self, object_: any, callbacks: list) -> None:
        for callback in callbacks:
            callback(object_, self)

    # Get the container's bindings.
    def getBindings(self) -> dict:
        return self._bindings

    # Get the alias for an abstract if available.
    def getAlias(self, abstract: str | callable) -> str:
        if abstract in self._aliases:
            return self.getAlias(self._aliases[abstract])

        return abstract

    # Get the extender callbacks for a given type.
    def _getExtenders(self, abstract: str) -> dict:
        if self.getAlias(abstract) in self._extenders:
            return self._extenders[abstract]

        return {}

    # Remove all of the extender callbacks for a given type.
    def forgetExtenders(self, abstract: str) -> None:
        self._extenders.pop(self.getAlias(abstract), None)

    # Drop all of the stale instances and aliases.
    def _dropStaleInstances(self, abstract: str) -> None:
        self._instances.pop(abstract, None)

        self._aliases.pop(abstract, None)

    # Remove a resolved instance from the instance cache.
    def forgetInstance(self, abstract: str) -> None:
        self._instances.pop(abstract, None)

    # Clear all of the instances from the container.
    def forgetInstances(self) -> None:
        self._instances = {}

    # Clear all of the scoped instances from the container.
    def forgetScopedInstances(self) -> None:
        for scoped in self._scopedInstances:
            self._instances.pop(scoped, None)

    # Flush the container of all bindings and resolved instances.
    def flush(self) -> None:
        self._aliases = {}
        self._resolved = []
        self._bindings = {}
        self._instances = {}
        self._abstractAliases = {}
        self._scopedInstances = []

    # Get the globally available instance of the container.
    @staticmethod
    def getInstance() -> ContainerContract:
        if Container.instance_ is None:
            Container.instance_ = Container()

        return Container.instance_

    # Set the shared instance of the container.
    @staticmethod
    def setInstance(container: ContainerContract = None) -> ContainerContract:
        Container.instance_ = container

        return Container.instance_

    # Determine if a given offset exists.
    def offsetExists(self, key: str) -> bool:
        return self.bound(key)

    # Get the value at a given offset.
    def offsetGet(self, key: str) -> any:
        return self.make(key)

    # Set the value at a given offset.
    def offsetSet(self, key: str, value: any) -> None:
        if not callable(value):
            value = lambda app: value

        self.bind(key, value)

    # Unset the value at a given offset.
    def offsetUnset(self, key: str) -> None:
        self._bindings.pop(key, None)

        self._instances.pop(key, None)

        if key in self._resolved:
            del self._resolved[self._resolved.index(key)]

    def __getitem__(self, key) -> any:
        return self.offsetGet(key)

    def __setitem__(self, key, value) -> None:
        self.offsetSet(key, value)

    def __delitem__(self, key) -> None:
        self.offsetUnset(key)

    # Dynamically access container services.
    def __get__(self, key: str) -> any:
        return self[key]

    # Dynamically set container services.
    def __set__(self, key: str, value: any) -> any:
        self[key] = value
