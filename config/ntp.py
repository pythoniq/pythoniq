from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'active': Env().get('NTP', False),
        'server': Env().get('NTP_SERVER', 'pool.ntp.org'),
        'port': Env().get('NTP_PORT', 123),
        'timeout': Env().get('NTP_TIMEOUT', 1),
    }

