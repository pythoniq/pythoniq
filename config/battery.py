from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'coin': {
            'rechargeable': False,
            'voltage': {
                'min': Env().get('BATTERY_COIN_MIN', 2),
                'max': Env().get('BATTERY_COIN_MAX', 3),
            },
        },
        'lipo': {
            'rechargeable': True,
            'voltage': {
                'min': Env().get('BATTERY_LIPO_MIN', 3),
                'max': Env().get('BATTERY_LIPO_MAX', 4.2),
            },
        },
    }
