from pythoniq.framework.illuminate.support.env import Env
from pythoniq.framework.illuminate.support.facades.app import App


def config():
    return {
        # --------------------------------------------------------------------------
        # Default Log Channel
        # --------------------------------------------------------------------------
        #
        # This option defines the default log channel that gets used when writing
        # messages to the logs. The name specified in this option should match
        # one of the channels defined in the "channels" configuration array.
        #
        'default': Env().get('LOG_CHANNEL', 'stack'),

        # --------------------------------------------------------------------------
        # Deprecations Log Channel
        # --------------------------------------------------------------------------
        #
        # This option controls the log channel that should be used to log warnings
        # regarding deprecated PHP and library features. This allows you to get
        # your application ready for upcoming major versions of dependencies.
        #
        'deprecations': {
            'channel': Env().get('LOG_DEPRECATIONS_CHANNEL', 'null'),
            'trace': False,
        },

        # --------------------------------------------------------------------------
        # Log Channels
        # --------------------------------------------------------------------------
        #
        # Here you may configure the log channels for your application. Out of
        # the box, Laravel uses the Monolog PHP logging library. This gives
        # you a variety of powerful log handlers / formatters to utilize.
        #
        # Available Drivers: "single", "daily", "slack", "syslog",
        #                    "errorlog", "monolog",
        #                    "custom", "stack"
        #
        'channels': {
            'stack': {
                'driver': 'stack',
                'channels': ['print', 'single'],
                'ignore_exceptions': False,
            },

            'print': {
                'driver': 'print',
                'level': 'debug',
            },

            'gsm': {
                'driver': 'daily',
                'path': App().storagePath('/logs/gsm.log'),
                'level': 'debug',
                'days': 7,
            },

            'meter': {
                'driver': 'daily',
                'path': App().storagePath('/logs/meter.log'),
                'level': 'debug',
                'days': 7,
            },

            'single': {
                'driver': 'single',
                'path': App().storagePath('/logs/pythoniq.log'),
                'level': Env().get('LOG_LEVEL', 'debug'),
                'replace_placeholders': True,
            },

            'daily': {
                'driver': 'daily',
                'path': App().storagePath('/logs/pythoniq.log'),
                'level': Env().get('LOG_LEVEL', 'debug'),
                'days': 14,
                'replace_placeholders': True,
            },

            'partition': {
                'driver': 'partition',
                'path': App().storagePath('/logs/pythoniq.log'),
                'level': Env().get('LOG_LEVEL', 'debug'),
                'lines': 10,
                'files': 3,
                'replace_placeholders': True,
            },

            'slack': {
                'driver': 'slack',
                'url': Env().get('LOG_SLACK_WEBHOOK_URL'),
                'username': Env().get('APP_NAME', 'Pythoniq') + ' Log',
                'emoji': ':boom:',
                'level': 'critical',
            },

            'ifttt': {
                'driver': 'ifttt',
                'url': Env().get('LOG_IFTTT_WEBHOOK_URL'),
                'level': 'critical',
            },
        }
    }

