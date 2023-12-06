from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'default': 'gridbox',

        'drivers': {
            'gridbox': {
                'driver': 'gridbox',
                'server': {
                    'host': Env().get('GRIDBOX_SERVER_HOST', '127.0.0.1'),
                    'port': Env().get('GRIDBOX_SERVER_PORT', 5000),
                }
            },
        }
    }
