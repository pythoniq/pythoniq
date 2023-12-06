from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'active': Env().get('NETWORK', False),
        'default': Env().get('NETWORK_DRIVER', 'wlan'),

        'drivers': {
            'wlan': {
                'driver': 'wlan',
                'active': Env().get('NETWORK_WLAN', False),
                'ssid': Env().get('NETWORK_WLAN_SSID', None),
                'password': Env().get('NETWORK_WLAN_PASSWORD', None),
                'config': {
                    'custom': Env().get('NETWORK_WLAN_CONFIG', False),
                    'ipv4': Env().get('NETWORK_WLAN_CONFIG_IPv4', None),
                    'gateway': Env().get('NETWORK_WLAN_CONFIG_GATEWAY', None),
                    'netmask': Env().get('NETWORK_WLAN_CONFIG_NETMASK', None),
                    'dns': Env().get('NETWORK_WLAN_CONFIG_DNS', None),
                },
            },

            'hotspot': {
                'driver': 'hotspot',
                'active': Env().get('NETWORK_HOTSPOT', False),
                'ssid': Env().get('NETWORK_HOTSPOT_SSID', None),
                'password': Env().get('NETWORK_HOTSPOT_PASSWORD', None),
            },
        }
    }

