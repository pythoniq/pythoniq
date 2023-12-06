from pythoniq.framework.illuminate.console.parser import Parser


class Command:
    # The Laravel application instance.
    _laravel = None

    # The name and signature of the console command.
    _signature = None

    # The console command name.
    _name = None

    # The console command description.
    _description = None

    # The console command help text.
    _help = None

    # Indicates whether the command should be shown in the Artisan command list.
    _hidden = False

    # Create a new console command instance.
    def __init__(self):
        # We will go ahead and set the name, description, and parameters on console
        # commands just to make things a little easier on the developer. This is
        # so they don't have to all be manually specified in the constructors.
        if self._signature is None:
            self._configureUsingFluentDefinition()
        else:
            super.__init__(self._name)

        # Once we have constructed the command, we'll set the description and other
        # related properties of the command. If a signature wasn't used to build
        # the command we'll set the arguments and the options on this command.
        if self._description is not None:
            self.setDescription(str(self.getDefaultDescription()))

        self.setHelp(str(self._help))

        if self._signature is None:
            self._specifyParameters()

        # if ($this instanceof Isolatable) {
        #     $this->configureIsolation();
        # }

    # Configure the console command using a fluent definition.
    def _configureUsingFluentDefinition(self) -> None:
        [name, arguments, options] = Parser.parse(self)

        self._name = name
        super.__init__(self._name)

        # After parsing the signature we will spin through the arguments and options
        # and set them on this command. These will already be changed into proper
        # instances of these "InputArgument" and "InputOption" Symfony classes.
        self.get
