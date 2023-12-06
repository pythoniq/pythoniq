from pythoniq.framework.illuminate.log.levels import Levels


class ParsesLogConfiguration(Levels):

    # Get fallback log channel name.
    def _getFallbackChannelName(self) -> str:
        raise NotImplementedError

    # Parse the string level into a Monolog constant.
    def _level(self, config: dict) -> int:
        level = config.get('level', 'debug')

        if level in self._levels:
            return self._levels['level']

        raise ValueError('Invalid log level.')

    # Parse the action level from the given configuration.
    def _actionLevel(self, config: dict) -> int:
        level = config.get('action_level', 'debug')

        if level in self._levels:
            return self._levels['level']

        raise ValueError('Invalid log action level.')

    # Extract the log channel from the given configuration.
    def _parseChannel(self, config: dict) -> str:
        return config['name'] or self._getFallbackChannelName()
